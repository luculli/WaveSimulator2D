# ---------------------------------------------------------------------
# -- Refactored Simulator
# ---------------------------------------------------------------------
# 1. Decoupled simulation components
#
# You can swap:
#   - Laplacian stencil
#   - CPU/GPU backend
#   - Integrators (FDTD, leapfrog, RK2, symplectic updates)
#   - Boundary conditions
# without touching WaveSimulator.
#
# 2. Scene objects no longer know about internals
#   - They simply modify a FieldSet.
#
# 3. Easier multi-GPU or batching
#   - Backend abstraction makes it possible.
#
# 4. Cleaner testing
#   - Mock backends let you test without CUDA.
# ---------------------------------------------------------------------


## Computation Backend
class ArrayBackend(ABC):
    @abstractmethod
    def array(self, data, dtype=None): pass

    @abstractmethod
    def zeros(self, shape, dtype=None): pass

    @abstractmethod
    def ones(self, shape, dtype=None): pass

    @abstractmethod
    def convolve2d(self, x, kernel): pass

class CuPyBackend(ArrayBackend):
    def __init__(self):
        import cupy as cp
        import cupyx.scipy.signal as cpsig
        self.cp = cp
        self.cp_signal = cpsig

    def array(self, data, dtype=None):
        return self.cp.array(data, dtype=dtype)

    def zeros(self, shape, dtype=None):
        return self.cp.zeros(shape, dtype=dtype)

    def ones(self, shape, dtype=None):
        return self.cp.ones(shape, dtype=dtype)

    def convolve2d(self, x, kernel):
        return self.cp_signal.convolve2d(x, kernel, mode="same", boundary="fill")

## 
class LaplacianOperator(ABC):
    @abstractmethod
    def apply(self, field): pass

class NinePointLaplacian(LaplacianOperator):
    def __init__(self, backend, kernel=None):
        self.backend = backend
        if kernel is None:
            kernel = [[0.066, 0.184, 0.066],
                      [0.184, -1.0, 0.184],
                      [0.066, 0.184, 0.066]]
        self.kernel = backend.array(kernel, dtype="float32")

    def apply(self, field):
        return self.backend.convolve2d(field, self.kernel)

## 
class TimeIntegrator(ABC):
    @abstractmethod
    def step(self, fields, laplacian, dt): pass

class StandardWaveIntegrator(TimeIntegrator):
    def step(self, F, lap, dt):
        # F is a FieldSet instance
        u, u_prev, c, d = F.u, F.u_prev, F.c, F.d
        
        # Laplacian
        L = lap.apply(u)

        # Velocity-like term
        v = (u - u_prev) * d * F.global_dampening

        # Update
        next_u = u + v + L * (c * dt)**2

        # Swap buffers
        F.u_prev[:] = u
        F.u[:] = next_u

## State
class FieldSet:
    def __init__(self, w, h, backend):
        self.backend = backend
        self.u       = backend.zeros((h, w), dtype="float32")
        self.u_prev  = backend.zeros((h, w), dtype="float32")
        self.c       = backend.ones((h, w), dtype="float32")
        self.d       = backend.ones((h, w), dtype="float32")
        self.global_dampening = 1.0

# Scene
class SceneObject(ABC):
    @abstractmethod
    def render_to_fields(self, fields: FieldSet): pass

    @abstractmethod
    def update_field(self, fields: FieldSet, t): pass

    @abstractmethod
    def draw_visualization(self, image: np.ndarray): pass

# Simulator
class WaveSimulator:
    def __init__(self, w, h, 
                 backend: ArrayBackend,
                 laplacian: LaplacianOperator,
                 integrator: TimeIntegrator,
                 scene_objects=None,
                 initial_field=None):

        self.backend     = backend
        self.laplacian   = laplacian
        self.integrator  = integrator
        self.fields      = FieldSet(w, h, backend)
        self.scene_objects = scene_objects or []
        self.t = 0.0
        self.dt = 1.0

        if initial_field is not None:
            self.fields.u[:] = initial_field
            self.fields.u_prev[:] = initial_field

    # -- Simulation Steps --

    def update_scene(self):
        F = self.fields

        # reset to defaults
        F.c.fill(1.0)
        F.d.fill(1.0)

        for obj in self.scene_objects:
            obj.render_to_fields(F)

        for obj in self.scene_objects:
            obj.update_field(F, self.t)

    def update_field(self):
        self.integrator.step(self.fields, self.laplacian, self.dt)
        self.t += self.dt

    # -- Accessors --

    def get_field(self):
        return self.fields.u

    def visualize_scene(self):
        image = np.zeros((*self.fields.c.shape, 3), dtype=np.uint8)
        for obj in self.scene_objects:
            obj.draw_visualization(image)
        return image


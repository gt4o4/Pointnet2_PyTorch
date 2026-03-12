import glob
import os
import os.path as osp

from setuptools import find_packages, setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

this_dir = osp.dirname(osp.abspath(__file__))
_ext_src_root = osp.join("pointnet2_ops", "_ext-src")
_ext_sources = glob.glob(osp.join(_ext_src_root, "src", "*.cpp")) + glob.glob(
    osp.join(_ext_src_root, "src", "*.cu")
)
_ext_headers = glob.glob(osp.join(_ext_src_root, "include", "*"))

requirements = ["torch>=1.4"]

exec(open(osp.join("pointnet2_ops", "_version.py")).read())

os.environ["TORCH_CUDA_ARCH_LIST"] = "7.5;8.0;8.6;8.9;9.0"
# PyTorch 2.10+ no longer adds CUDA_HOME/include for the host compiler.
_cuda_home = os.environ.get("CUDA_HOME") or os.environ.get("CUDA_PATH")
_cuda_inc = osp.join(_cuda_home, "include") if _cuda_home and osp.isdir(osp.join(_cuda_home, "include")) else None
setup(
    name="pointnet2_ops",
    version=__version__,
    author="Erik Wijmans",
    packages=find_packages(),
    install_requires=requirements,
    ext_modules=[
        CUDAExtension(
            name="pointnet2_ops._ext",
            sources=_ext_sources,
            extra_compile_args={
                "cxx": ["-O3"],
                "nvcc": ["-O3", "-Xfatbin", "-compress-all"],
            },
            include_dirs=[d for d in [osp.join(this_dir, _ext_src_root, "include"), _cuda_inc] if d],
        )
    ],
    cmdclass={"build_ext": BuildExtension},
    include_package_data=True,
)

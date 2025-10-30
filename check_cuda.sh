#!/bin/bash
# CUDA Version Check Script

echo "=== CUDA Installation Check ==="
echo ""

# Check CUDA version
echo "1. CUDA Toolkit Version:"
if command -v nvcc &> /dev/null; then
    nvcc --version
else
    echo "   nvcc not found in PATH"
fi
echo ""

# Check NVIDIA driver
echo "2. NVIDIA Driver Version:"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=driver_version --format=csv,noheader
else
    echo "   nvidia-smi not found"
fi
echo ""

# Full GPU info
echo "3. GPU Information:"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi
else
    echo "   nvidia-smi not found"
fi
echo ""

# Check CUDA library path
echo "4. CUDA Library Path:"
if [ -d "/usr/local/cuda" ]; then
    echo "   /usr/local/cuda exists"
    ls -la /usr/local/cuda/lib64/libcudart.so* 2>/dev/null || echo "   cudart library not found"
else
    echo "   /usr/local/cuda not found"
fi
echo ""

# Check LD_LIBRARY_PATH
echo "5. LD_LIBRARY_PATH:"
echo "   $LD_LIBRARY_PATH"
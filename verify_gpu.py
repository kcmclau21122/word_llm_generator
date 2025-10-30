#!/usr/bin/env python3
"""
GPU Verification Script
Checks CUDA availability and PyTorch GPU support
"""

import sys
import subprocess


def check_cuda_version():
    """Check CUDA version using nvidia-smi."""
    print("=" * 70)
    print("CUDA AND GPU VERIFICATION")
    print("=" * 70)
    print()
    
    try:
        # Get CUDA version from nvidia-smi
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=driver_version,name,memory.total', '--format=csv,noheader'],
            capture_output=True,
            text=True,
            check=True
        )
        
        driver, gpu_name, memory = result.stdout.strip().split(', ')
        print(f"✓ NVIDIA Driver Version: {driver}")
        print(f"✓ GPU: {gpu_name}")
        print(f"✓ GPU Memory: {memory}")
        print()
        
        # Get CUDA runtime version
        cuda_result = subprocess.run(
            ['nvidia-smi'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Extract CUDA version from nvidia-smi output
        for line in cuda_result.stdout.split('\n'):
            if 'CUDA Version:' in line:
                cuda_version = line.split('CUDA Version:')[1].strip().split()[0]
                print(f"✓ CUDA Version: {cuda_version}")
                print()
                return cuda_version
                
    except subprocess.CalledProcessError:
        print("✗ nvidia-smi command failed")
        print("  Make sure NVIDIA drivers are installed")
        return None
    except FileNotFoundError:
        print("✗ nvidia-smi not found")
        print("  Make sure NVIDIA drivers are installed and in PATH")
        return None


def check_pytorch():
    """Check if PyTorch is installed and has CUDA support."""
    print("-" * 70)
    print("PYTORCH GPU SUPPORT CHECK")
    print("-" * 70)
    print()
    
    try:
        import torch
        
        print(f"✓ PyTorch installed: {torch.__version__}")
        print(f"✓ CUDA available: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"✓ CUDA version (PyTorch): {torch.version.cuda}")
            print(f"✓ Number of GPUs: {torch.cuda.device_count()}")
            
            for i in range(torch.cuda.device_count()):
                print(f"  - GPU {i}: {torch.cuda.get_device_name(i)}")
                props = torch.cuda.get_device_properties(i)
                print(f"    Memory: {props.total_memory / 1024**3:.2f} GB")
                print(f"    Compute Capability: {props.major}.{props.minor}")
            
            print()
            print("✓ PyTorch GPU support is properly configured!")
            return True
        else:
            print("✗ CUDA not available in PyTorch")
            print("  You may need to reinstall PyTorch with CUDA support")
            return False
            
    except ImportError:
        print("✗ PyTorch not installed")
        print("  Run: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
        return False


def check_ollama():
    """Check Ollama GPU support."""
    print("-" * 70)
    print("OLLAMA GPU SUPPORT CHECK")
    print("-" * 70)
    print()
    
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✓ Ollama is installed")
        print()
        print("Installed models:")
        print(result.stdout)
        
        print("Note: Ollama automatically uses GPU if CUDA is available")
        print("      No additional configuration needed")
        return True
        
    except FileNotFoundError:
        print("✗ Ollama not found")
        print("  Install from: https://ollama.ai/download")
        return False
    except subprocess.CalledProcessError:
        print("✗ Ollama command failed")
        return False


def test_gpu_inference():
    """Test actual GPU inference."""
    print()
    print("-" * 70)
    print("GPU INFERENCE TEST")
    print("-" * 70)
    print()
    
    try:
        import torch
        
        if not torch.cuda.is_available():
            print("⚠ CUDA not available, skipping test")
            return
        
        print("Testing GPU tensor operations...")
        
        # Create tensor on GPU
        device = torch.device('cuda')
        x = torch.randn(1000, 1000, device=device)
        y = torch.randn(1000, 1000, device=device)
        
        # Perform operation
        z = torch.matmul(x, y)
        
        print(f"✓ Successfully performed matrix multiplication on GPU")
        print(f"  Device: {z.device}")
        print(f"  Shape: {z.shape}")
        print()
        
        # Memory info
        print(f"GPU Memory Allocated: {torch.cuda.memory_allocated() / 1024**2:.2f} MB")
        print(f"GPU Memory Reserved: {torch.cuda.memory_reserved() / 1024**2:.2f} MB")
        
    except Exception as e:
        print(f"✗ GPU inference test failed: {str(e)}")


def main():
    """Run all checks."""
    # Check CUDA
    cuda_version = check_cuda_version()
    
    # Check PyTorch
    print()
    pytorch_ok = check_pytorch()
    
    # Check Ollama
    print()
    check_ollama()
    
    # Test GPU if PyTorch is available
    if pytorch_ok:
        test_gpu_inference()
    
    print()
    print("=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)
    print()
    
    if cuda_version and pytorch_ok:
        print("✓ Your system is ready for GPU-accelerated LLM inference!")
        print()
        print("Recommended next steps:")
        print("1. Pull Ollama models: ollama pull deepseek-r1:7b")
        print("2. Run the application: streamlit run app.py")
        print("3. Ollama will automatically use your GPU")
    else:
        print("⚠ GPU support needs configuration")
        print()
        print("Next steps:")
        if not cuda_version:
            print("1. Install NVIDIA drivers and CUDA toolkit")
        if not pytorch_ok:
            print("2. Install PyTorch with CUDA: see GPU_SETUP.md")
        print("3. Re-run this script to verify")


if __name__ == "__main__":
    main()
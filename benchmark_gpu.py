#!/usr/bin/env python3
"""
GPU Benchmark Script
Tests your RTX GPU performance with PyTorch
"""

import time
import sys


def check_cuda():
    """Check if CUDA is available."""
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        print("ERROR: PyTorch not installed")
        print("Install with: pip install -r requirements-gpu-cu121.txt --extra-index-url https://download.pytorch.org/whl/cu121")
        return False


def run_benchmark():
    """Run GPU benchmark."""
    import torch
    
    if not torch.cuda.is_available():
        print("ERROR: CUDA not available")
        print("See GPU_SETUP.md for troubleshooting")
        sys.exit(1)
    
    device = torch.device('cuda')
    gpu_name = torch.cuda.get_device_name(0)
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
    
    print("=" * 70)
    print("GPU PERFORMANCE BENCHMARK")
    print("=" * 70)
    print()
    print(f"GPU: {gpu_name}")
    print(f"Memory: {gpu_memory:.2f} GB")
    print(f"CUDA Version: {torch.version.cuda}")
    print()
    
    # Test different matrix sizes
    sizes = [1000, 2000, 5000, 8000]
    
    print("Running matrix multiplication benchmarks...")
    print()
    print(f"{'Size':<10} {'Time (ms)':<15} {'Memory (MB)':<15} {'TFLOPS':<10}")
    print("-" * 70)
    
    for size in sizes:
        # Warmup
        x = torch.randn(size, size, device=device)
        y = torch.randn(size, size, device=device)
        z = torch.matmul(x, y)
        torch.cuda.synchronize()
        
        # Clear memory
        torch.cuda.empty_cache()
        
        # Benchmark
        iterations = 10
        start = time.time()
        
        for _ in range(iterations):
            z = torch.matmul(x, y)
        
        torch.cuda.synchronize()
        end = time.time()
        
        avg_time = (end - start) / iterations * 1000
        memory_mb = torch.cuda.memory_allocated() / 1024**2
        
        # Calculate TFLOPS (2 * size^3 operations)
        flops = 2 * size ** 3
        tflops = (flops / (avg_time / 1000)) / 1e12
        
        print(f"{size:<10} {avg_time:<15.2f} {memory_mb:<15.2f} {tflops:<10.2f}")
    
    print()
    print("=" * 70)
    print("BENCHMARK COMPLETE")
    print("=" * 70)
    print()
    
    # Performance rating
    print("Performance Rating:")
    if avg_time < 100:
        print("✓ Excellent - Your GPU is performing great!")
    elif avg_time < 200:
        print("✓ Good - Solid performance for LLM inference")
    elif avg_time < 300:
        print("⚠ Fair - Consider checking GPU drivers and cooling")
    else:
        print("⚠ Poor - See GPU_SETUP.md troubleshooting section")
    
    print()
    print("Expected performance for RTX GPUs:")
    print("  RTX 4090:  ~10-15ms (8000x8000)")
    print("  RTX 4080:  ~15-20ms (8000x8000)")
    print("  RTX 4070:  ~20-30ms (8000x8000)")
    print("  RTX 3080:  ~25-35ms (8000x8000)")
    print()


def main():
    """Main entry point."""
    if not check_cuda():
        sys.exit(1)
    
    try:
        run_benchmark()
    except Exception as e:
        print(f"ERROR: Benchmark failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
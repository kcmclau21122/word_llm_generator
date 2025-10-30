# GPU Setup Guide for NVIDIA RTX GPUs

## Overview

Your NVIDIA GeForce RTX GPU with 16GB memory is perfect for running local LLMs with Ollama. This guide will help you set up GPU acceleration for optimal performance.

## Quick GPU Verification

### Step 1: Check Your CUDA Version

Run the bash script:
```bash
./check_cuda.sh
```

Or check manually:
```bash
# Method 1: Check CUDA compiler version
nvcc --version

# Method 2: Check from nvidia-smi
nvidia-smi

# Method 3: Check CUDA runtime
cat /usr/local/cuda/version.txt  # If file exists
```

**Look for**: `CUDA Version: X.X` (e.g., 12.1, 11.8)

### Step 2: Verify GPU Detection

```bash
nvidia-smi
```

You should see output like:
```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 545.29.06              Driver Version: 545.29.06      CUDA Version: 12.3     |
|-------------------------------+----------------------+--------------------------------+
| GPU  Name                 TCC/WDDM  | Bus-Id        Disp.A | Volatile Uncorr. ECC     |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M.   |
|===============================+======================+================================|
|   0  NVIDIA GeForce RTX...    On    | 00000000:01:00.0  On |                  N/A     |
| 30%   45C    P8              12W / 320W |    500MiB / 16384MiB |      0%      Default   |
+-------------------------------+----------------------+--------------------------------+
```

**Key information:**
- **GPU Name**: Your RTX model
- **Memory**: Should show 16384MiB (16GB)
- **CUDA Version**: Your CUDA runtime version

## Installation Steps

### Option A: Automatic Setup with Verification Script

```bash
# Make script executable
chmod +x verify_gpu.py

# Run verification
python3 verify_gpu.py
```

This will:
1. Check CUDA installation
2. Verify GPU detection
3. Check PyTorch GPU support
4. Test GPU inference
5. Check Ollama installation
6. Provide installation guidance if needed

### Option B: Manual Setup

#### 1. Determine Your CUDA Version

```bash
nvidia-smi | grep "CUDA Version"
```

Note the version (e.g., 12.1 or 11.8)

#### 2. Install GPU-Accelerated PyTorch

**For CUDA 12.1 or newer:**
```bash
pip install -r requirements-gpu-cu121.txt --extra-index-url https://download.pytorch.org/whl/cu121
```

**For CUDA 11.8:**
```bash
pip install -r requirements-gpu-cu118.txt --extra-index-url https://download.pytorch.org/whl/cu118
```

**For other CUDA versions:**
Visit https://pytorch.org/get-started/locally/ and use their installer selector.

#### 3. Verify PyTorch GPU Support

```python
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
```

Should output:
```
CUDA available: True
GPU: NVIDIA GeForce RTX 4080
```

## Ollama GPU Configuration

### Good News: Ollama Auto-Detects GPU

Ollama automatically uses your GPU if CUDA is available. **No additional configuration needed!**

### Verify Ollama GPU Usage

```bash
# Start Ollama
ollama serve

# In another terminal, pull a model
ollama pull deepseek-r1:7b

# Run inference and watch GPU usage
# Terminal 1: Monitor GPU
watch -n 1 nvidia-smi

# Terminal 2: Run model
ollama run deepseek-r1:7b "Write a short poem"
```

**Expected behavior:**
- GPU utilization spikes during inference
- GPU memory usage increases
- Much faster responses than CPU

### Ollama GPU Memory Configuration

If you have multiple GPUs or want to limit memory:

```bash
# Set GPU to use (if you have multiple)
export CUDA_VISIBLE_DEVICES=0

# Limit GPU memory (optional)
export OLLAMA_GPU_LAYERS=35  # Adjust based on model size

# Start Ollama
ollama serve
```

## Performance Expectations

### With Your 16GB RTX GPU

| Model Size | Fits in VRAM? | Speed |
|------------|---------------|-------|
| 7B models (DeepSeek-R1:7b) | ✅ Yes | Very Fast (30-50 tokens/s) |
| 13B models | ✅ Yes | Fast (15-30 tokens/s) |
| 34B models | ⚠️ Tight | Moderate (5-15 tokens/s) |
| 70B+ models | ❌ No (requires offloading) | Slow |

**Recommended for 16GB:** 7B and 13B models for best experience

### Recommended Models for Your GPU

```bash
# Excellent performance
ollama pull deepseek-r1:7b
ollama pull llama3.3:8b
ollama pull mistral:7b
ollama pull gemma2:9b

# Good performance
ollama pull llama3.1:13b
ollama pull mixtral:8x7b  # Uses MoE, fits well

# Will work but slower
ollama pull llama3.1:70b  # Will use CPU offloading
```

## Troubleshooting

### Issue 1: "CUDA not available" in PyTorch

**Diagnosis:**
```python
import torch
print(torch.cuda.is_available())  # Returns False
```

**Solutions:**

1. **Wrong PyTorch version installed:**
   ```bash
   pip uninstall torch torchvision torchaudio
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

2. **CUDA toolkit not in PATH:**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export PATH=/usr/local/cuda/bin:$PATH
   export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
   
   # Reload
   source ~/.bashrc
   ```

3. **Version mismatch:**
   - PyTorch CUDA version must be ≤ your installed CUDA version
   - Check: `nvcc --version` vs `torch.version.cuda`

### Issue 2: Ollama Not Using GPU

**Diagnosis:**
```bash
# Run model and check nvidia-smi in another terminal
ollama run deepseek-r1:7b "test"

# If GPU-Util stays at 0%, GPU not being used
```

**Solutions:**

1. **CUDA not detected by Ollama:**
   ```bash
   # Check Ollama can see CUDA
   ollama list
   
   # Reinstall Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Environment variables blocking GPU:**
   ```bash
   # Remove these if set
   unset CUDA_VISIBLE_DEVICES
   unset OLLAMA_NUM_GPU
   
   # Restart Ollama
   pkill ollama
   ollama serve
   ```

3. **Driver issues:**
   ```bash
   # Update NVIDIA drivers
   # Ubuntu/Debian:
   sudo apt update
   sudo apt install nvidia-driver-545
   
   # Reboot required
   sudo reboot
   ```

### Issue 3: Out of Memory Errors

**Error:** `CUDA out of memory`

**Solutions:**

1. **Use smaller model:**
   ```bash
   ollama pull deepseek-r1:7b  # Instead of larger variants
   ```

2. **Reduce context window:**
   ```bash
   # In config.json, reduce max_tokens
   "generation": {
     "max_tokens": 1000  # Instead of 2000
   }
   ```

3. **Enable GPU memory offloading:**
   ```bash
   export OLLAMA_GPU_LAYERS=30  # Offload some layers to CPU
   ```

### Issue 4: Slow Performance Despite GPU

**Diagnosis:**
GPU showing in nvidia-smi but inference still slow

**Solutions:**

1. **Check GPU utilization:**
   ```bash
   watch -n 0.5 nvidia-smi
   # Should see 80-100% during inference
   ```

2. **PCIe bandwidth bottleneck:**
   ```bash
   nvidia-smi -q | grep -A 3 "GPU Current"
   # Should show PCIe Gen 3 or 4 with x16 lanes
   ```

3. **CPU bottleneck:**
   ```bash
   # Monitor CPU while running
   htop
   # If CPU at 100%, may be preprocessing bottleneck
   ```

4. **Model not fully loaded in VRAM:**
   ```bash
   # Check memory usage
   nvidia-smi
   # Model should use several GB, not just hundreds of MB
   ```

## Advanced Configuration

### Multiple GPUs

If you have multiple GPUs:

```bash
# Use specific GPU
export CUDA_VISIBLE_DEVICES=0  # Use first GPU
export CUDA_VISIBLE_DEVICES=1  # Use second GPU
export CUDA_VISIBLE_DEVICES=0,1  # Use both

# Or in Python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
```

### Mixed Precision (Faster Inference)

For supported models:

```bash
# Ollama automatically uses optimal precision
# 16GB GPU typically uses FP16 or BF16 automatically
```

### Monitor GPU Temperature

```bash
# Watch temperature
watch -n 1 'nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader'

# If >80°C consistently, improve cooling
```

## Configuration Updates for GPU

### Update config.json

No changes needed! The application automatically uses GPU when available.

However, you can optimize generation parameters:

```json
{
  "generation": {
    "temperature": 0.7,
    "max_tokens": 2000,  # Can increase with GPU (try 4000)
    "top_p": 0.9
  }
}
```

### Environment Variables (Optional)

Create `.env` file:

```bash
# GPU Configuration
CUDA_VISIBLE_DEVICES=0
OLLAMA_GPU_LAYERS=35

# OpenAI (if using)
OPENAI_API_KEY=your-key-here
```

## Verification Checklist

Before running the application, verify:

- [ ] `nvidia-smi` shows your GPU
- [ ] `nvcc --version` shows CUDA toolkit
- [ ] `python verify_gpu.py` shows all checks passing
- [ ] PyTorch detects CUDA: `python -c "import torch; print(torch.cuda.is_available())"`
- [ ] Ollama installed: `ollama --version`
- [ ] Model pulled: `ollama pull deepseek-r1:7b`
- [ ] GPU used during inference: monitor with `nvidia-smi`

## Performance Benchmarking

### Test GPU Performance

```python
# Create benchmark.py
import torch
import time

if not torch.cuda.is_available():
    print("CUDA not available!")
    exit(1)

device = torch.device('cuda')
print(f"Testing on: {torch.cuda.get_device_name(0)}")

# Warmup
x = torch.randn(5000, 5000, device=device)
y = torch.randn(5000, 5000, device=device)
z = torch.matmul(x, y)
torch.cuda.synchronize()

# Benchmark
iterations = 100
start = time.time()

for _ in range(iterations):
    z = torch.matmul(x, y)
    
torch.cuda.synchronize()
end = time.time()

avg_time = (end - start) / iterations * 1000
print(f"Average time per operation: {avg_time:.2f} ms")
print(f"GPU Memory Used: {torch.cuda.memory_allocated() / 1024**2:.2f} MB")

# Your RTX GPU should complete this in 10-30ms per iteration
```

Run:
```bash
python benchmark.py
```

### Expected Results

**RTX 4080 (16GB):** ~15-20ms per iteration  
**RTX 4070 Ti (16GB):** ~20-30ms per iteration  
**RTX 3080 (16GB):** ~25-35ms per iteration  

## Additional Resources

### NVIDIA Tools

```bash
# Detailed GPU info
nvidia-smi -L

# Monitor power, temp, utilization
nvidia-smi dmon

# GPU topology (for multi-GPU)
nvidia-smi topo -m
```

### PyTorch GPU Utilities

```python
import torch

# Current device
torch.cuda.current_device()

# Device count
torch.cuda.device_count()

# Device name
torch.cuda.get_device_name(0)

# Memory stats
torch.cuda.memory_summary(device=0)

# Clear cache
torch.cuda.empty_cache()
```

### Ollama GPU Info

```bash
# Check Ollama GPU support
ollama info

# List running models and memory
ollama ps

# Check logs for GPU messages
journalctl -u ollama -f  # If using systemd
```

## Next Steps

1. **Run verification:** `python verify_gpu.py`
2. **Pull model:** `ollama pull deepseek-r1:7b`
3. **Test locally:** `ollama run deepseek-r1:7b "test"`
4. **Monitor GPU:** `watch -n 1 nvidia-smi`
5. **Run application:** `streamlit run app.py`

Your 16GB RTX GPU is excellent for running 7B-13B models with great performance! 🚀

## Support

If you encounter issues:

1. Check logs: `cat logs/app_*.log`
2. Run verification: `python verify_gpu.py`
3. Check GPU: `nvidia-smi`
4. Monitor during inference: `watch -n 1 nvidia-smi`
5. Test PyTorch: `python -c "import torch; torch.cuda.is_available()"`
# GPU Acceleration Setup - Quick Reference

## Your Hardware: NVIDIA RTX GPU (16GB)

Perfect for running local LLMs! Your GPU can handle 7B-13B models with excellent performance.

## 🚀 Quick Setup (3 Steps)

### 1. Check CUDA Version
```bash
nvidia-smi
```
Look for "CUDA Version: X.X" in the output

### 2. Install GPU Requirements
```bash
# Activate your venv first
source venv/bin/activate

# For CUDA 12.1+ (most common for recent drivers)
pip install -r requirements-gpu-cu121.txt --extra-index-url https://download.pytorch.org/whl/cu121

# For CUDA 11.8
pip install -r requirements-gpu-cu118.txt --extra-index-url https://download.pytorch.org/whl/cu118
```

### 3. Verify Setup
```bash
# Make executable
chmod +x verify_gpu.py

# Run verification
python verify_gpu.py
```

**Expected Output:**
```
✓ NVIDIA Driver Version: 545.29.06
✓ GPU: NVIDIA GeForce RTX 4080
✓ GPU Memory: 16000 MiB
✓ CUDA Version: 12.1
✓ PyTorch installed: 2.5.1
✓ CUDA available: True
✓ PyTorch GPU support is properly configured!
```

## 📋 What Got Installed

### New Files:
- `requirements-gpu-cu121.txt` - GPU requirements for CUDA 12.1+
- `requirements-gpu-cu118.txt` - GPU requirements for CUDA 11.8
- `GPU_SETUP.md` - Comprehensive GPU setup guide
- `verify_gpu.py` - GPU verification script
- `benchmark_gpu.py` - GPU performance benchmark
- `check_cuda.sh` - CUDA version checker (bash)

### Updated Files:
- `requirements.txt` - Now notes GPU options
- `QUICKSTART.md` - GPU setup instructions added

## 🎯 Performance Expectations

| Model | VRAM Usage | Speed (tokens/s) |
|-------|------------|------------------|
| deepseek-r1:7b | ~4-5 GB | 30-50 |
| llama3.3:8b | ~5-6 GB | 25-40 |
| mistral:7b | ~4-5 GB | 30-45 |
| llama3.1:13b | ~8-10 GB | 15-30 |
| mixtral:8x7b | ~10-12 GB | 20-35 |

## ✅ Verification Checklist

Run these commands to verify everything works:

```bash
# 1. GPU detected
nvidia-smi

# 2. CUDA version
nvcc --version

# 3. Complete verification
python verify_gpu.py

# 4. Performance test (optional)
python benchmark_gpu.py

# 5. Ollama GPU test
ollama pull deepseek-r1:7b
ollama run deepseek-r1:7b "test GPU inference"
# Watch GPU usage: watch -n 1 nvidia-smi
```

## 🔧 Ollama GPU Usage

**Good news:** Ollama automatically uses your GPU! No configuration needed.

### Verify Ollama Uses GPU:

**Terminal 1 - Monitor GPU:**
```bash
watch -n 1 nvidia-smi
```

**Terminal 2 - Run Inference:**
```bash
ollama run deepseek-r1:7b "Write a haiku about computers"
```

**What to look for in nvidia-smi:**
- GPU-Util should spike to 80-100%
- Memory-Usage should increase by several GB
- Power usage should increase

## 📊 Benchmark Your GPU

```bash
# Run benchmark
python benchmark_gpu.py
```

**Expected results for RTX GPUs:**
- RTX 4090: ~10-15ms (excellent)
- RTX 4080: ~15-20ms (excellent)
- RTX 4070 Ti: ~20-30ms (great)
- RTX 3080: ~25-35ms (good)

## 🐛 Quick Troubleshooting

### GPU Not Used
```bash
# Check PyTorch sees GPU
python -c "import torch; print(torch.cuda.is_available())"
# Should print: True

# If False, reinstall GPU requirements
pip uninstall torch torchvision torchaudio
pip install -r requirements-gpu-cu121.txt --extra-index-url https://download.pytorch.org/whl/cu121
```

### Ollama Not Using GPU
```bash
# Check Ollama is running
pgrep ollama

# Restart Ollama
pkill ollama
ollama serve
```

### Out of Memory
```bash
# Use smaller model
ollama pull deepseek-r1:7b  # Instead of larger variants

# Or reduce context in config.json
"max_tokens": 1000
```

## 📖 Documentation

- **GPU_SETUP.md** - Comprehensive GPU setup guide (start here!)
- **QUICKSTART.md** - Updated with GPU instructions
- **verify_gpu.py** - Automated verification
- **benchmark_gpu.py** - Performance testing

## 🎓 Recommended Models for 16GB GPU

```bash
# Best performance (highly recommended)
ollama pull deepseek-r1:7b
ollama pull llama3.3:8b
ollama pull mistral:7b

# Good performance
ollama pull llama3.1:13b
ollama pull gemma2:9b

# Works but uses more memory
ollama pull mixtral:8x7b
```

## 💡 Pro Tips

1. **Monitor GPU usage during first run:**
   ```bash
   watch -n 0.5 nvidia-smi
   ```

2. **Check GPU temperature:**
   ```bash
   nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader
   ```
   Keep it under 80°C for sustained workloads

3. **Clear GPU memory between runs:**
   ```bash
   python -c "import torch; torch.cuda.empty_cache()"
   ```

4. **See detailed GPU info:**
   ```bash
   nvidia-smi -q | less
   ```

## 🚦 Status Indicators

### All Working:
```
✓ nvidia-smi shows GPU
✓ verify_gpu.py passes all checks  
✓ GPU-Util spikes during Ollama inference
✓ Fast response times (30+ tokens/s for 7B models)
```

### Needs Attention:
```
✗ nvidia-smi fails → Install/update NVIDIA drivers
✗ CUDA not available in PyTorch → Wrong PyTorch version
✗ GPU-Util stays at 0% → Ollama not using GPU
✗ Slow inference → Check GPU drivers and cooling
```

## 🎉 Ready to Use!

Once all checks pass:
```bash
streamlit run app.py
```

Your GPU will automatically accelerate:
- Ollama model inference (30-50x faster than CPU)
- Faster document processing
- Better responsiveness

## 📞 Need Help?

1. **Read:** `GPU_SETUP.md` (comprehensive troubleshooting)
2. **Run:** `python verify_gpu.py` (automated diagnostics)
3. **Check:** `logs/app_*.log` (application logs)
4. **Monitor:** `nvidia-smi` (real-time GPU status)

---

**Your 16GB RTX GPU is perfect for this application! 🚀**

Expect 5-10x faster inference compared to CPU-only operation with 7B models.
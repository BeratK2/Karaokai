import numpy as np
import librosa

def calculate_sdr(reference, estimated):
    """Calculate Signal-to-Distortion Ratio (SDR) in dB."""
    # --- Ensure same length --- 
    min_len = min(len(reference), len(estimated))
    reference, estimated = reference[:min_len], estimated[:min_len]
    
    # --- Calculate SDR --- 
    ref_energy = np.sum(reference**2)
    error_energy = np.sum((reference - estimated)**2)
    
    return 10 * np.log10(ref_energy / error_energy) if error_energy > 0 else float('inf')


# --- Load audio files with consistent parameters ---
original, sample_rate_orig = librosa.load('./test_songs/LEEONA_-_LEEONA_-_Do_I.mp3', sr=None, mono=False)
processed, sample_rate_proc = librosa.load('./separated/htdemucs/LEEONA_-_LEEONA_-_Do_I/no_vocals.wav', sr=None, mono=False)


# --- Ensure same sample rate ---
if sample_rate_orig != sample_rate_proc:
    print(f"Warning: Sample rates differ ({sample_rate_orig} Hz vs {sample_rate_proc} Hz). Resampling processed audio.")
    processed = librosa.resample(processed, orig_sr=sample_rate_proc, target_sr=sample_rate_orig)


# --- Handle mono or stereo ---
if len(original.shape) > 1 and len(processed.shape) > 1:
    # Both are stereo
    sdrs = [calculate_sdr(original[ch], processed[ch]) for ch in range(min(original.shape[0], processed.shape[0]))]
    print(f"Channel SDRs: {[f'{sdr:.2f} dB' for sdr in sdrs]}, Average: {np.mean(sdrs):.2f} dB")
elif len(original.shape) > 1:
    # Original is stereo, processed is mono
    original_mono = np.mean(original, axis=0)
    sdr = calculate_sdr(original_mono, processed)
    print(f"SDR (original converted to mono): {sdr:.2f} dB")
elif len(processed.shape) > 1:
    # Original is mono, processed is stereo
    processed_mono = np.mean(processed, axis=0)
    sdr = calculate_sdr(original, processed_mono)
    print(f"SDR (processed converted to mono): {sdr:.2f} dB")
else:
    # Both are mono
    sdr = calculate_sdr(original, processed)
    print(f"SDR: {sdr:.2f} dB")
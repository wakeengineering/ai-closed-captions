# Speaker Separation Research Notes

**Date:** January 29, 2026  
**Status:** Research complete, implementation deferred

## Goal
Investigate using pyannote speaker embeddings to create speaker-specific audio chunks for cleaner transcription, especially for overlapping speech segments.

## Findings

### What's Available

#### 1. Pyannote Embedding Model (`pyannote/embedding`)
- **Dimension:** 512
- **Architecture:** `XVectorSincNet` (ECAPA-TDNN style)
- **Chunk duration:** 5.0 seconds
- **Can extract embeddings from raw waveforms:**
  ```python
  from pyannote.audio import Model, Inference
  emb_model = Model.from_pretrained('pyannote/embedding', token=hf_token)
  # Direct waveform input: (batch, channel, samples)
  embedding = emb_model(waveform.unsqueeze(0))  # Output: (1, 512)
  ```

#### 2. SpeechBrain SepformerSeparation
- **Type:** Blind source separation (no speaker embedding input)
- **Available models:**
  - `speechbrain/sepformer-wsj02mix` - 2 speakers
  - `speechbrain/sepformer-wsj03mix` - 3 speakers  
  - `speechbrain/sepformer-wham` - 2 speakers + noise
- **Key methods:** `separate_file(path)`, `separate_batch(mix)`

#### 3. SpeechBrain SpeakerRecognition
- Available for speaker verification/identification
- Can compute embeddings for matching

### What's NOT Available
- **Target Speaker Extraction (TSE)** models that take a speaker embedding and extract only that speaker's voice
- SpeechBrain 1.0.3 doesn't have built-in TSE inference classes

## Proposed Hybrid Approach

For handling overlapping speech:

1. **Detect overlapping segments** from pyannote diarization output
2. **For overlapping segments only:** Run SepFormer blind separation → get 2-3 separated audio sources
3. **Build speaker profiles:** Extract pyannote embeddings from non-overlapping segments for each speaker
4. **Match separated sources to speakers:** Compute embeddings of separated sources, compare via cosine similarity to known speaker embeddings
5. **Assign to correct speaker** based on highest similarity

### Pseudocode
```python
def separate_overlapping_segment(overlap_audio, speaker_profiles):
    # speaker_profiles = {speaker_id: embedding_tensor}
    
    # 1. Blind separation
    separated_sources = sepformer.separate_batch(overlap_audio)  # (N_sources, samples)
    
    # 2. Compute embeddings for each separated source
    source_embeddings = [emb_model(src) for src in separated_sources]
    
    # 3. Match to known speakers
    assignments = {}
    for src_idx, src_emb in enumerate(source_embeddings):
        best_speaker = None
        best_sim = -1
        for speaker_id, profile_emb in speaker_profiles.items():
            sim = cosine_similarity(src_emb, profile_emb)
            if sim > best_sim:
                best_sim = sim
                best_speaker = speaker_id
        assignments[src_idx] = (best_speaker, best_sim)
    
    return separated_sources, assignments
```

## Dependencies Installed
- `omegaconf` - Required for pyannote embedding model loading
- `speechbrain==1.0.3` - Already installed as pyannote dependency

## Complexity Assessment
- **High complexity:** Requires managing speaker profiles, handling edge cases
- **Performance impact:** SepFormer adds significant compute time per overlap
- **For anime dubs:** Overlapping speech is typically rare

## Recommendation
Keep current diarization approach. Only implement hybrid separation if:
1. Significant overlapping speech issues are encountered
2. Current quality is insufficient for specific content types

## Alternative Approaches to Consider Later
1. **Time-domain speaker beamforming** - If multi-channel audio available
2. **Fine-tuned TSE model** - Train custom target speaker extraction
3. **Commercial APIs** - Services like AssemblyAI offer speaker separation

## Related Files
- [transcribe_faster_whisper.py](../transcribe_faster_whisper.py) - Main pipeline
- [private/ai-closed-captions.conf](../private/ai-closed-captions.conf) - Config with HF tokens

## References
- [pyannote-audio docs](https://github.com/pyannote/pyannote-audio)
- [SpeechBrain separation](https://speechbrain.github.io/tutorials/source-separation.html)
- [SepFormer paper](https://arxiv.org/abs/2010.13154)

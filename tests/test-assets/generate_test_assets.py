import audsp
import audiofile as af
import sox

dur = 1.0
channel_list = [1, 2]
sr_list = [8000, 16000, 44100]

for n_ch in channel_list:
    for sr_in in sr_list:
        wav_original = f'original__sr_{sr_in}__channels_{n_ch}.wav'
        x = audsp.utils.am_fm_synth(
            dur, num_channels=n_ch, sampling_rate=sr_in
        )
        af.write(wav_original, x, sr_in)
        for sr_out in sr_list:
            if sr_out == sr_in:
                continue
            wav = f'resampled__sr-in_{sr_in}__sr-out_{sr_out}__channels' \
                  f'_{n_ch}.wav'
            tfm = sox.Transformer()
            tfm.rate(sr_out)
            tfm.build(wav_original, wav)

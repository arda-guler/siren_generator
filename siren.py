from synthesizer import Player, Synthesizer, Waveform
import math
pi = math.pi

player = Player()
player.open_stream()

synth1 = Synthesizer(osc1_waveform = Waveform.sine, osc1_volume=0.1,
                     use_osc2=True, osc2_waveform=Waveform.square, osc2_volume=0.5)

class alarm_constant_tone:
    def __init__(self, pitch, volume=100):
        self.pitch = pitch
        self.volume = volume

    def play(self):
        while True:
            player.play_wave(synth1.generate_constant_wave(self.pitch, 1))

class alarm_constant_interrupted:
    def __init__(self, pitch, length_play, length_interrupt, volume=100):
        self.pitch = pitch
        self.length_play = length_play
        self.length_interrupt = length_interrupt
        self.volume = volume

    def play(self):
        while True:
            player.play_wave(synth1.generate_constant_wave(self.pitch, self.length_play))
            player.play_wave(synth1.generate_constant_wave(0, self.length_interrupt))

class alarm_constant_alternating: # airliner master alarm
    def __init__(self, pitch1, length1, pitch2, length2, volume=100):
        self.pitch1 = pitch1
        self.length1 = length1
        self.pitch2 = pitch2
        self.length2 = length2
        self.volume = volume

    def play(self):
        while True:
            player.play_wave(synth1.generate_constant_wave(self.pitch1, self.length1))
            player.play_wave(synth1.generate_constant_wave(self.pitch2, self.length2))

class alarm_rising_pitch:
    def __init__(self, pitch_low, pitch_high, length, volume=100):
        self.pitch_low = pitch_low
        self.pitch_high = pitch_high
        self.length = length
        self.volume = volume

    def play(self):
        dl = 0.01
        curr_l = 0
        while True:
            if curr_l > self.length:
                curr_l = 0
                
            current_pitch = self.pitch_low + curr_l * (self.pitch_high - self.pitch_low)
            player.play_wave(synth1.generate_constant_wave(current_pitch, dl))
            curr_l += dl

class alarm_lowering_pitch:
    def __init__(self, pitch_low, pitch_high, length, volume=100):
        self.pitch_low = pitch_low
        self.pitch_high = pitch_high
        self.length = length
        self.volume = volume

    def play(self):
        dl = 0.01
        curr_l = 0
        while True:
            if curr_l > self.length:
                curr_l = 0
                
            current_pitch = self.pitch_high - curr_l * (self.pitch_high - self.pitch_low)
            player.play_wave(synth1.generate_constant_wave(current_pitch, dl))
            curr_l += dl

class alarm_cyclic_wail:
    def __init__(self, pitch_low, pitch_high, length, volume=100):
        self.pitch_low = pitch_low
        self.pitch_high = pitch_high
        self.length = length
        self.volume = volume

    def play(self):
        dl = 0.01
        curr_l = 0
        while True:
            if curr_l > self.length:
                curr_l = 0

            angle = curr_l * pi / self.length
            current_pitch = self.pitch_low + math.sin(angle) * (self.pitch_high - self.pitch_low)
            player.play_wave(synth1.generate_constant_wave(current_pitch, dl))
            curr_l += dl

class alarm_alternate_wail: # tornado siren
    def __init__(self, pitch_low, pitch_high, length, volume=100):
        self.pitch_low = pitch_low
        self.pitch_high = pitch_high
        self.length = length
        self.volume = volume

    def play(self):
        dl = 0.02
        curr_l = 0
        while True:
            if curr_l > self.length:
                curr_l = 0

            angle1 = curr_l * pi / self.length
            angle2 = (curr_l * pi / self.length) + pi/12
            current_pitch1 = self.pitch_low + math.sin(angle1) * (self.pitch_high - self.pitch_low)
            current_pitch2 = self.pitch_low + math.sin(angle2) * (self.pitch_high - self.pitch_low)

            if (curr_l / self.length) % 0.2 < 0.1:
                player.play_wave(synth1.generate_constant_wave(current_pitch1, dl))
            else:
                player.play_wave(synth1.generate_constant_wave(current_pitch2, dl))
                
            curr_l += dl

print("Alarms:")
print("1) Constant tone")
print("2) Interrupted constant tone")
print("3) Alternating constant tone (Master Caution)")
print("4) Rising pitch")
print("5) Lowering pitch")
print("6) Cyclic wail (Air Raid/Nuclear Siren)")
print("7) Alternate wail (Tornado Siren)")

selection = int(input(" > "))

if selection == 1:
    current_alarm = alarm_constant_tone(450)
elif selection == 2:
    current_alarm = alarm_constant_interrupted(450, 0.2, 0.2)
elif selection == 3:
    current_alarm = alarm_constant_alternating(200, 0.2, 600, 0.2)
elif selection == 4:
    current_alarm = alarm_rising_pitch(200, 600, 1)
elif selection == 5:
    current_alarm = alarm_lowering_pitch(200, 600, 1)
elif selection == 6:
    current_alarm = alarm_cyclic_wail(200, 600, 10)
elif selection == 7:
    current_alarm = alarm_alternate_wail(200, 600, 10)
    
current_alarm.play()

from flask import Flask, request, jsonify, render_template, send_from_directory, abort
from music21 import instrument, note, stream, chord
import random
import os
import subprocess
from pydub import AudioSegment
from datetime import datetime
import logging

app = Flask(__name__)

# Setup basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set the folder where generated MIDI and MP3 files will be stored
cur_dir=os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
sound_font = os.path.join(os.getcwd(), 'soundfonts', 'GeneralUserGs.sf2')  # Path to the SoundFont file
fluidsynth_path = os.path.join(cur_dir, 'fluidsynth', 'bin', 'fluidsynth.exe')
# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def generate_random_pitch(scale):
    return random.choice(scale)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/generate', methods=['GET'])
def generate_music():
    num_notes = int(request.args.get('num_notes', 30))
    scale_type = request.args.get('scale', 'C_major')
    selected_instrument = request.args.get('instrument', 'Piano')
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Generate a timestamp
    
     

    #scales
    scales = {
        'C_major': ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5'],
        'G_major': ['G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F#4', 'G4'],
        'A_minor': ['A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4', 'A4'],
        'Blues': ['C4', 'Eb4', 'F4', 'Gb4', 'G4', 'Bb4'],
        'Pentatonic': ['C4', 'D4', 'E4', 'G4', 'A4', 'C5']
    }

   #can you add multiple tracks and scales and more instruments?
    # combined.insert(0, midi1) I believe this is how you play two tracks at once!
    # combined.insert(0, midi2)
    scale = scales.get(scale_type)
    if not scale:
        return jsonify({"error": "Invalid scale type provided"}), 400

    music_stream = stream.Stream()

    # Set the instrument based on user input or default
    instrument_map = {'violin': instrument.Violin, 'guitar': instrument.Guitar, 'piano': instrument.Piano}
    music_stream.insert(0, instrument_map.get(selected_instrument.lower(), instrument.Piano)())

    for i in range(num_notes):
        pitch = generate_random_pitch(scale)
        music_note = note.Note(pitch)
        music_stream.append(music_note)

    midi_filename = f'output_{timestamp}.mid'
    midi_path = os.path.join(app.config['UPLOAD_FOLDER'], midi_filename)
    music_stream.write('midi', fp=midi_path)
    # Use FluidSynth to convert MIDI to WAV
    wav_path = midi_path.replace('.mid', '.wav')
    try:
        subprocess.run([fluidsynth_path, '-ni', sound_font, midi_path, '-F', wav_path, '-r', '44100'], check=True)
    except subprocess.CalledProcessError as e:
        logging.error("Failed to convert MIDI to WAV: %s", str(e))
        return jsonify({"error": "Failed to convert MIDI to WAV", "exception": str(e)}), 500

    # Convert WAV to MP3 using pydub
    try:
        sound = AudioSegment.from_file(wav_path)
        mp3_path = wav_path.replace('.wav', '.mp3')
        sound.export(mp3_path, format="mp3")
    except Exception as e:
        logging.error("Failed to convert WAV to MP3: %s", str(e))
        return jsonify({"error": "Failed to convert MIDI to MP3", "exception": str(e)}), 500

    return jsonify({"message": "Music generated", "file": mp3_path.replace(os.getcwd() + '/', '')})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.isfile(file_path):
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

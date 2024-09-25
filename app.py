from flask import Flask, request, send_file
import librosa
import soundfile as sf
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mix_music():
    if request.method == 'POST':
        # Get the uploaded files
        pattern_file = request.files['pattern']
        sound_file = request.files['sound']
        
        # Load the audio files
        pattern, sr = librosa.load(pattern_file, sr=None)
        sound, _ = librosa.load(sound_file, sr=sr)
        
        # Make sure sound is as long as pattern
        if len(sound) < len(pattern):
            sound = np.tile(sound, int(np.ceil(len(pattern)/len(sound))))
        sound = sound[:len(pattern)]
        
        # Mix: just multiply them for now
        mixed = pattern * sound
        
        # Save the result
        sf.write('result.wav', mixed, sr)
        
        # Send the file back
        return send_file('result.wav', as_attachment=True)
    
    # If it's a GET request, show a simple form
    return '''
        <form method="post" enctype="multipart/form-data">
            Pattern: <input type="file" name="pattern"><br>
            Sound: <input type="file" name="sound"><br>
            <input type="submit" value="Mix">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
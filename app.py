from flask import Flask, render_template, jsonify
import geocoder

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_location')
def get_location():
    try:
        g = geocoder.ip('me')
        if g.latlng:
            return jsonify({
                'lat': g.latlng[0],
                'lng': g.latlng[1],
                'address': g.address or "Localização por IP",
                'accuracy': "IP"
            })
    except:
        pass
    return jsonify({
        'lat': -23.5505,  # São Paulo como fallback
        'lng': -46.6333,
        'address': 'São Paulo, SP (fallback)',
        'accuracy': 'Fallback'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
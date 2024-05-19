import requests
import logging
import subprocess
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def test_generate_music(num_notes=30, scale='G_major', instrument='Guitar'):
    #   DEFINED THE API Endpoint URL
    url = "http://127.0.0.1:5000/generate"

    # Parameters for the music generation
    params = {
        'num_notes': num_notes,
        'scale': scale,
        'instrument': instrument
    }

    try:
        # Make the GET request
        response = requests.get(url, params=params)

        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            print("Success: Music generated.")
            print("Response Data:", response_data)  # Assumes response is JSON

            # Download and play the music file if available
            if 'file' in response_data:
                music_url = f"http://127.0.0.1:5000/{response_data['file']}"  # Corrected URL
                music_response = requests.get(music_url)
                if music_response.status_code == 200:
                    music_path = os.path.join('downloads', os.path.basename(response_data['file']))
                    if not os.path.exists('downloads'):
                        os.makedirs('downloads')
                    with open(music_path, 'wb') as f:
                        f.write(music_response.content)
                    print("Music file downloaded, playing now...")
                    subprocess.run(
                        ['open', music_path])  # 'open' works on macOS, use 'start' on Windows or 'xdg-open' on Linux
                else:
                    print("Failed to download the music file.")
            else:
                print("No music file in response.")

            logging.info(f"Music generated successfully with parameters: {params}")
        else:
            print("Failed to generate music. Status code:", response.status_code)
            logging.error(f"Failed to generate music. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("HTTP Request failed:", e)
        logging.error(f"HTTP Request failed: {e}")


if __name__ == "__main__":
    test_generate_music()  # Default parameters can be changed here for different tests

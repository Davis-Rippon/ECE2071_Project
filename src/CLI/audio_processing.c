#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>


// Should be twice the highest frequency (could be lower ~8000Hz)
#define SAMPLE_RATE 44100
// Number of values being pushed into moving average filter each time
#define SAMPLE_LENGTH 10


typedef struct {
    char riffHeader[4]; // Contains "RIFF"
    uint32_t wavSize; // Size of the wav portion of the file, which follows the first 8 bytes. File size - 8
    char waveHeader[4]; // Contains "WAVE"
    char fmtHeader[4]; // Contains "fmt " (includes trailing space)
    uint32_t fmtChunkSize; // Should be 16 for PCM
    uint16_t audioFormat; // Should be 1 for PCM. 3 for IEEE Float
    uint16_t numChannels;
    uint32_t sampleRate;
    uint32_t byteRate;  // Number of bytes per second. sampleRate * numChannels * Bytes Per Sample
    uint16_t sampleAlignment; // numChannels * Bytes Per Sample
    uint16_t bitDepth; // Number of bits per sample
    char dataHeader[4]; // Contains "data"
    uint32_t dataSize; // Number of bytes in data. Number of samples * numChannels * sample byte size
} WavHeader;


void write_wav_header(const char* filename, float* data, int numSamples);
void moving_average(float* data, int dataSize, float* result);


int main() {
    FILE* inputFile = fopen("data/test.data", "r");
    if (!inputFile) {
        perror("DATA FILE ERROR");
        return -1;
    }

    FILE* outputFile = fopen("output.csv", "w");
    if (!outputFile) {
        fclose(inputFile);
        perror("CSV FILE ERROR");
        return -1;
    }

    float* data = malloc(sizeof(float) * 1024);
    float* filteredData = malloc(sizeof(float) * 1024);
    int numSamples = 0;
    int capacity = 1024;

    while (fscanf(inputFile, "%f", &data[numSamples]) != EOF) {
        if (numSamples < capacity) {
            data[numSamples] = data[numSamples]; // **PLACEHOLDER FOR ACTUAL READING LOGIC**
            // **SHOULD ONLY COUNT BETWEEN FLAGS FOR VOLTAGES; NOT US READINGS**
            numSamples++;
            if (numSamples == capacity) {
                capacity *= 2;
                data = realloc(data, sizeof(float) * capacity);
                filteredData = realloc(filteredData, sizeof(float) * capacity);
            }
        }
    }

    moving_average(data, numSamples, filteredData);

    for (int i = 0; i < numSamples - SAMPLE_LENGTH + 1; i++) {
        fprintf(outputFile, "%f, %f\n", data[i], filteredData[i]);
    }

    write_wav_header("output.wav", filteredData, numSamples - SAMPLE_LENGTH + 1);

    free(data);
    free(filteredData);
    fclose(inputFile);
    fclose(outputFile);

    return 0;
}


void write_wav_header(const char* filename, float* data, int numSamples) {
    FILE* file = fopen(filename, "wb");
    if (!file) {
        perror("WAV FILE ERROR");
        return;
    }

    // Prepare WAV header
    WavHeader header;
    int byteDepth = sizeof(float);

    strncpy(header.riffHeader, "RIFF", 4);
    strncpy(header.waveHeader, "WAVE", 4);
    strncpy(header.fmtHeader, "fmt ", 4);
    header.fmtChunkSize = 16;
    header.audioFormat = 1;
    // Monophonic
    header.numChannels = 1;
    header.sampleRate = SAMPLE_RATE;
    header.byteRate = SAMPLE_RATE * header.numChannels * byteDepth;
    header.sampleAlignment = header.numChannels * byteDepth;
    header.bitDepth = byteDepth * 8;
    strncpy(header.dataHeader, "data", 4);
    header.dataSize = numSamples * byteDepth;
    header.wavSize = header.dataSize + 36;

    fwrite(&header, sizeof(WavHeader), 1, file);
    fwrite(data, sizeof(float), numSamples, file);
    fclose(file);
}


void moving_average(float* data, int dataSize, float* result) {
    // Voltages will be read as floats
    float sum = 0.0;
    for (int i = 0; i < SAMPLE_LENGTH && i < dataSize; i++) {
        sum += data[i];
    }

    // Moving average for current point
    for (int i = 0; i < dataSize - SAMPLE_LENGTH + 1; i++) {
        result[i] = sum / SAMPLE_LENGTH;
        // Move to next point
        if (i + SAMPLE_LENGTH < dataSize) {
            sum = sum - data[i] + data[i + SAMPLE_LENGTH];
        }
    }
}

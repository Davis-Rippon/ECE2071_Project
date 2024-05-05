#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>


// Number of values being pushed into moving average filter each time
#define SAMPLE_LENGTH 10
#define US_MIN_VALUE 9999
#define US_MAX_VALUE 30000
#define ADC_MIN_VALUE 0
#define ADC_MAX_VALUE 4095

int SAMPLE_RATE = 6000;


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


void write_wav_header(const char* filename, int16_t* data, int numSamples, int isFiltered);
void moving_average(int16_t* data, int dataSize, int16_t* result);



int main(int argc, char *args[]) {

    if (argc != 3) {
        printf("Incorrect number of arguments provided. Two arguments expected.");
        return 1;
    }

    FILE* inputFile = fopen(args[1],"r");

    if (!inputFile) {
        perror("DATA FILE ERROR");
        return -1;
    }

    SAMPLE_RATE = atoi(args[2]);

    FILE* usOutputFile = fopen("us_data.csv", "w");
    if (!usOutputFile) {
        fclose(inputFile);
        perror("US CSV FILE ERROR");
        return -1;
    }

    // Temp capacity
    int arraySize = 1024;
    int16_t* data = malloc(sizeof(int16_t) * arraySize);
    int16_t* adcData = malloc(sizeof(int16_t) * arraySize);
    int16_t* filteredAdcData = malloc(sizeof(int16_t) * arraySize);
    int numValues = 0;
    int numValuesUS = 0;
    int numValuesADC = 0;

    // Read .data file
    while (fscanf(inputFile, "%hd", &data[numValues]) != EOF) {
        if (data[numValues] >= US_MIN_VALUE && data[numValues] <= US_MAX_VALUE) {
            // US Data
            fprintf(usOutputFile, "%hd\n", data[numValues]);
            numValuesUS++;
        } else if (data[numValues] >= ADC_MIN_VALUE && data[numValues] <= ADC_MAX_VALUE) {
            // ADC Data
            adcData[numValuesADC++] = data[numValues];
        }
        if (numValues < arraySize) {
            numValues++;
            // Data file almost certainly bigger than temp capacity, so need to adjust array size
            if (numValues == arraySize) {
                arraySize *= 2;
                data = realloc(data, sizeof(int16_t) * arraySize);
                adcData = realloc(adcData, sizeof(int16_t) * arraySize);
                filteredAdcData = realloc(filteredAdcData, sizeof(int16_t) * arraySize);
            }
        }
    }

    fclose(inputFile);
    fclose(usOutputFile);

    // Create RAW ADC .wav file
    write_wav_header("raw_adc_data.wav", adcData, numValuesADC, 0);

    // Filter ADC data
    moving_average(adcData, numValuesADC, filteredAdcData);

    // Create filtered ADC .wav file
    write_wav_header("filtered_adc_data.wav", filteredAdcData, numValuesADC - SAMPLE_LENGTH + 1, 1);

    free(data);
    free(adcData);
    free(filteredAdcData);

    return 0;
}


void write_wav_header(const char* filename, int16_t* data, int numValues, int isFiltered) {
    FILE* file = fopen(filename, "wb");
    if (!file) {
        perror("WAV FILE ERROR");
        return;
    }

    // Prepare WAV header
    WavHeader header;
    int byteDepth = sizeof(int16_t);

    strncpy(header.riffHeader, "RIFF", 4);
    strncpy(header.waveHeader, "WAVE", 4);
    strncpy(header.fmtHeader, "fmt ", 4);
    header.fmtChunkSize = 16;
    // Writing with 16-bit ints
    header.audioFormat = 1;
    // Monophonic
    header.numChannels = 1;
    header.sampleRate = SAMPLE_RATE;
    header.byteRate = SAMPLE_RATE * header.numChannels * byteDepth;
    header.sampleAlignment = header.numChannels * byteDepth;
    header.bitDepth = byteDepth * 8;
    strncpy(header.dataHeader, "data", 4);
    header.dataSize = numValues * byteDepth;
    header.wavSize = header.dataSize + 36;

    fwrite(&header, sizeof(WavHeader), 1, file);
    fwrite(data, sizeof(int16_t), numValues, file);
    fclose(file);
}


void moving_average(int16_t* data, int dataSize, int16_t* result) {
    int sum = 0;
    for (int i = 0; i < SAMPLE_LENGTH && i < dataSize; i++) {
        sum += data[i];
    }

    for (int i = 0; i < dataSize - SAMPLE_LENGTH + 1; i++) {
        result[i] = sum / SAMPLE_LENGTH;
        if (i + SAMPLE_LENGTH < dataSize) {
            sum = sum - data[i] + data[i + SAMPLE_LENGTH];
        }
    }
}

#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"

const float conversion_factor = 3.3f / (1 << 12);
const int num_samples = 10;  // Define the number of samples to average

void printhelp()
{
    puts("\nCommands:");
    puts("0\t: read ADC 0");
    puts("1\t: read ADC 1");
}

void read_with_offset_correction(int adc_channel) {
    uint16_t signal_sum = 0;
    uint16_t ground_sum = 0;

    // Take multiple samples and compute their sum
    for (int i = 0; i < num_samples; i++) {
        // Read Signal
        adc_select_input(adc_channel);
        signal_sum += adc_read();

        // Read Ground reference to correct offset
        adc_select_input(2);
        ground_sum += adc_read();
    }

    // Calculate average
    uint16_t signal = signal_sum / num_samples;
    uint16_t ground = ground_sum / num_samples;

    // Ensure no overflow close to 0 V
    uint16_t offset = MIN(signal, ground);

    // Correct the signal
    uint16_t corrected_signal = signal - offset;
    float voltage = corrected_signal * conversion_factor;

    // Calculate and print Voltage to serial
    printf("%f\n", voltage);
}


int main(void)
{
    stdio_init_all();
    adc_init();
    adc_set_temp_sensor_enabled(false);

    // Set all pins to input (as far as SIO is concerned)
    gpio_set_dir_all_bits(0);
    for (int i = 2; i < 30; ++i)
    {
        gpio_set_function(i, GPIO_FUNC_SIO);
        if (i >= 26)
        {
            gpio_disable_pulls(i);
            gpio_set_input_enabled(i, false);
        }
    }

// initialize onboard LED default on
#ifdef PICO_DEFAULT_LED_PIN
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
    gpio_put(PICO_DEFAULT_LED_PIN, 1);
#endif

    // Set SMPS Pin high for PWM_mode to increase Vref stability
    gpio_init(23);
    gpio_set_dir(23, GPIO_OUT);
    gpio_put(23, 1);


    printf("\n===========================\n");
    printf("RP2040 ADC and Test Console\n");
    printf("===========================\n");
    printhelp();

    while (1)
    {
        char recievedChar = getchar();
        switch (recievedChar)
        {
        case '0':
        {
            read_with_offset_correction(0);
            break;
        }
        case '1':
            read_with_offset_correction(1);
            break;
        case '\n':
        case '\r':
            break;
        case 'h':
            printhelp();
            break;
        default:
            printf("\nUnrecognised command: %c\n", recievedChar);
            printhelp();
            break;
        }
    #ifdef PICO_DEFAULT_LED_PIN
        // Blink LED
        gpio_put(PICO_DEFAULT_LED_PIN, 0);
        sleep_ms(50);
        gpio_put(PICO_DEFAULT_LED_PIN, 1);
    #endif
    }
}

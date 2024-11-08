#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"

#define N_SAMPLES 1000
uint16_t sample_buf[N_SAMPLES];

void printhelp()
{
    puts("\nCommands:");
    puts("s\t: Sample once");
}

void __not_in_flash_func(adc_capture)(uint16_t *buf, size_t count)
{
    adc_fifo_setup(true, false, 0, false, false);
    adc_run(true);
    for (size_t i = 0; i < count; i = i + 1)
        buf[i] = adc_fifo_get_blocking();
    adc_run(false);
    adc_fifo_drain();
}

int main(void)
{
    stdio_init_all();
    adc_init();
    adc_set_temp_sensor_enabled(false);
    adc_select_input(0);

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

    printf("\n===========================\n");
    printf("RP2040 ADC and Test Console\n");
    printf("===========================\n");
    printhelp();

    while (1)
    {
        char recievedChar = getchar();
        switch (recievedChar)
        {
        case 's':
        {
            uint32_t result = adc_read();
            const float conversion_factor = 3.3f / (1 << 12);
            printf("%f\n", result, result * conversion_factor);
            break;
        }
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

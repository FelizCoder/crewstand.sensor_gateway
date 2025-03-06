
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/uart.h"
#include "hardware/adc.h"

// UART defines
#define UART_ID uart0
#define BAUD_RATE 250000

// Pins can be changed, see the GPIO function select table in the datasheet for information on GPIO assignments
#define UART_TX_PIN 16
#define UART_RX_PIN 17

const float conversion_factor = 3.3f / (1 << 12);
const int num_samples = 10; // Define the number of samples to average

void init_uart()
{
    // Set up our UART
    uart_init(UART_ID, BAUD_RATE);
    // Set the TX and RX pins by using the function select on the GPIO
    // Set datasheet for more information on function select
    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);
}

void printhelp()
{
    puts("\nCommands:");
    puts("0\t: read ADC channel 0");
    puts("1\t: read ADC channel 1");
    puts("s\t: read both ADC channels");
}

uint16_t read_and_average(int adc_channel)
{
    uint16_t signal_sum = 0;
    adc_select_input(adc_channel);

    // Take multiple samples and compute their sum
    for (int i = 0; i < num_samples; i++)
    {
        signal_sum += adc_read();
    }

    // Calculate average
    const uint16_t signal = signal_sum / num_samples;
    return signal;
}

float corrected_voltage(int signal, int ground)
{
    // Ensure no overflow close to 0 V
    const uint16_t offset = MIN(signal, ground);
    // Correct the signal
    const uint16_t corrected_signal = signal - offset;
    // Calculate voltage
    const float voltage = corrected_signal * conversion_factor;

    return voltage;
}

void print_voltage_with_offset_correction(int adc_channel)
{
    const uint16_t signal = read_and_average(adc_channel);
    const uint16_t ground = read_and_average(2);
    const float voltage = corrected_voltage(signal, ground);
    // Voltage to serial
    printf("%f\n", voltage);
}

void print_both_with_offset_correction()
{
    const uint16_t signal_0 = read_and_average(0);
    const uint16_t signal_1 = read_and_average(1);
    const uint16_t ground = read_and_average(2);
    // Calculate voltages
    const float voltage_0 = corrected_voltage(signal_0, ground);
    const float voltage_1 = corrected_voltage(signal_1, ground);
    // Voltage to serial
    printf("%f,%f\n", voltage_0, voltage_1);
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

#ifdef PICO_DEFAULT_LED_PIN
    // initialize onboard LED default on
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
    gpio_put(PICO_DEFAULT_LED_PIN, 1);
#endif

    // Set SMPS Pin high for PWM_mode to increase Vref stability
    gpio_init(23);
    gpio_set_dir(23, GPIO_OUT);
    gpio_put(23, 1);

    init_uart();

    printhelp();

    while (1)
    {
        char recievedChar = getchar();
        switch (recievedChar)
        {
        case '0':
        {
            print_voltage_with_offset_correction(0);
            break;
        }
        case '1':
        {
            print_voltage_with_offset_correction(1);
            break;
        }
        case 's':
        {
            print_both_with_offset_correction();
            break;
        };
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

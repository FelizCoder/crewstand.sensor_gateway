# Changelog

## [2.1.0](https://github.com/FelizCoder/crewstand.sensor_gateway/compare/v2.0.0...v2.1.0) (2024-12-10)


### Features

* **adc:** add case and logic read both sensors at once ([4c3d50f](https://github.com/FelizCoder/crewstand.sensor_gateway/commit/4c3d50fd5bdfdd9db36cb149c86eaf5e14bb9e9d)), closes [#12](https://github.com/FelizCoder/crewstand.sensor_gateway/issues/12)
* **adc:** implement sampling and averaging for ADC readings ([3c07d18](https://github.com/FelizCoder/crewstand.sensor_gateway/commit/3c07d1862790f7ba672e07f0dc8a91346f89805f)), closes [#11](https://github.com/FelizCoder/crewstand.sensor_gateway/issues/11)
* **host:** enhance sensor reading and logging functionality ([63105cf](https://github.com/FelizCoder/crewstand.sensor_gateway/commit/63105cf49d90c31af2a1752a9d43defd3f983f57)), closes [#12](https://github.com/FelizCoder/crewstand.sensor_gateway/issues/12)

## [2.0.0](https://github.com/FelizCoder/crewstand.sensor_gateway/compare/v1.0.0...v2.0.0) (2024-12-03)


### ⚠ BREAKING CHANGES

* **adc_console:** Listening to `0` and `1` on Serial to request sensor reading

### Features

* **adc_console:** add offset correction and support for 2 sensors ([9fa9b80](https://github.com/FelizCoder/crewstand.sensor_gateway/commit/9fa9b80f6cfed349fbfafef1e4de1b7f2b30c6fe))
* **sensor:** add multi-sensor support and update backend URL configuration ([d4dedd0](https://github.com/FelizCoder/crewstand.sensor_gateway/commit/d4dedd008d6b5c3b88e26c7b869826bbf684c4e1))
* **sensor:** incorporate interpolation and voltage reading functionality ([268be91](https://github.com/FelizCoder/crewstand.sensor_gateway/commit/268be916ae344b8e7d013022dc016f1e832b51cd)), closes [#9](https://github.com/FelizCoder/crewstand.sensor_gateway/issues/9)

## 1.0.0 (2024-11-08)


### Bug Fixes

* remove extra quotes from environment variable values ([140cd68](https://github.com/FelizCoder/crewstand.sensor_gateway/commit/140cd68246998af9352adda4b621783f1aaa89c3))

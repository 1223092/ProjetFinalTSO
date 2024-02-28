EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:R R1
U 1 1 6216C3D3
P 5050 2850
F 0 "R1" H 5120 2896 50  0000 L CNN
F 1 "4.7k" H 5120 2805 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder" V 4980 2850 50  0001 C CNN
F 3 "~" H 5050 2850 50  0001 C CNN
	1    5050 2850
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 6216D831
P 5350 2850
F 0 "R2" H 5420 2896 50  0000 L CNN
F 1 "4.7k" H 5420 2805 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder" V 5280 2850 50  0001 C CNN
F 3 "~" H 5350 2850 50  0001 C CNN
	1    5350 2850
	1    0    0    -1  
$EndComp
$Comp
L Device:R R3
U 1 1 6216E02B
P 5650 4250
F 0 "R3" V 5750 4200 50  0000 L CNN
F 1 "4.7k" V 5550 4200 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder" V 5580 4250 50  0001 C CNN
F 3 "~" H 5650 4250 50  0001 C CNN
	1    5650 4250
	0    -1   -1   0   
$EndComp
Text Label 5200 2400 0    50   ~ 0
3V3
Wire Wire Line
	5200 2650 5200 2400
Wire Wire Line
	4600 3400 5050 3400
Wire Wire Line
	5050 3400 5050 3000
Wire Wire Line
	4600 3500 5350 3500
Wire Wire Line
	5350 3500 5350 3000
Wire Wire Line
	5050 2700 5050 2650
Wire Wire Line
	5050 2650 5200 2650
Wire Wire Line
	5350 2700 5350 2650
Wire Wire Line
	5350 2650 5200 2650
Connection ~ 5200 2650
Wire Wire Line
	5050 3400 5150 3400
Connection ~ 5050 3400
Wire Wire Line
	5350 3500 5450 3500
Connection ~ 5350 3500
Text Label 5150 3400 0    50   ~ 0
SDA
Text Label 5450 3500 0    50   ~ 0
SCL
$Comp
L Connector_Generic:Conn_01x04 J201
U 1 1 6219CA7E
P 7500 3250
F 0 "J201" H 7580 3242 50  0000 L CNN
F 1 "Conn_01x04" H 7580 3151 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 7500 3250 50  0001 C CNN
F 3 "~" H 7500 3250 50  0001 C CNN
	1    7500 3250
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x04 J203
U 1 1 6219D7FF
P 7500 2750
F 0 "J203" H 7580 2742 50  0000 L CNN
F 1 "Conn_01x04" H 7580 2651 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 7500 2750 50  0001 C CNN
F 3 "~" H 7500 2750 50  0001 C CNN
	1    7500 2750
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x04 J202
U 1 1 6219F271
P 8700 3250
F 0 "J202" H 8780 3242 50  0000 L CNN
F 1 "Conn_01x04" H 8780 3151 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 8700 3250 50  0001 C CNN
F 3 "~" H 8700 3250 50  0001 C CNN
	1    8700 3250
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x04 J204
U 1 1 6219F277
P 8700 2750
F 0 "J204" H 8780 2742 50  0000 L CNN
F 1 "Conn_01x04" H 8780 2651 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 8700 2750 50  0001 C CNN
F 3 "~" H 8700 2750 50  0001 C CNN
	1    8700 2750
	1    0    0    -1  
$EndComp
Text Label 7300 2650 2    50   ~ 0
SCL
Text Label 7300 2750 2    50   ~ 0
SDA
Text Label 8500 2650 2    50   ~ 0
SCL
Text Label 8500 2750 2    50   ~ 0
SDA
Text Label 7300 3150 2    50   ~ 0
SCL
Text Label 7300 3250 2    50   ~ 0
SDA
Text Label 8500 3150 2    50   ~ 0
SCL
Text Label 8500 3250 2    50   ~ 0
SDA
Text Label 3400 5450 0    50   ~ 0
GND
Text Label 7300 2850 2    50   ~ 0
GND
Text Label 7300 2950 2    50   ~ 0
3V3
Text Label 7300 3350 2    50   ~ 0
GND
Text Label 7300 3450 2    50   ~ 0
3V3
Text Label 8500 3350 2    50   ~ 0
GND
Text Label 8500 3450 2    50   ~ 0
3V3
Text Label 8500 2850 2    50   ~ 0
GND
Text Label 8500 2950 2    50   ~ 0
3V3
Text Label 7300 3750 2    50   ~ 0
3V3
Text Label 7300 3850 2    50   ~ 0
GPIO
Text Label 7300 3950 2    50   ~ 0
GND
Text Label 7300 4350 2    50   ~ 0
3V3
Text Label 7300 4450 2    50   ~ 0
GPIO
Text Label 7300 4550 2    50   ~ 0
GND
Text Label 7300 4950 2    50   ~ 0
3V3
Text Label 7300 5150 2    50   ~ 0
GND
Text Label 8500 3750 2    50   ~ 0
3V3
Text Label 8500 3850 2    50   ~ 0
GPIO
Text Label 8500 3950 2    50   ~ 0
GND
Text Label 8500 4350 2    50   ~ 0
3V3
Text Label 8500 4450 2    50   ~ 0
GPIO
Text Label 8500 4550 2    50   ~ 0
GND
Text Label 8500 4950 2    50   ~ 0
3V3
Text Label 8500 5050 2    50   ~ 0
GPIO
Text Label 8500 5150 2    50   ~ 0
GND
Text Label 5900 4900 0    50   ~ 0
GPIO
Text Label 5900 5000 0    50   ~ 0
GPIO
Text Label 5900 5100 0    50   ~ 0
GPIO
Text Label 4600 3700 0    50   ~ 0
GPIO4
Text Label 4600 3800 0    50   ~ 0
GPIO5
Text Label 4600 3900 0    50   ~ 0
GPIO6
Text Label 5400 4900 2    50   ~ 0
GPIO4
Text Label 5400 5000 2    50   ~ 0
GPIO5
Text Label 5400 5100 2    50   ~ 0
GPIO6
NoConn ~ 3000 3100
NoConn ~ 3000 3200
NoConn ~ 3000 3400
NoConn ~ 3000 3500
NoConn ~ 3000 3600
NoConn ~ 3000 3800
NoConn ~ 3000 3900
NoConn ~ 3000 4000
NoConn ~ 3000 4200
NoConn ~ 3000 4300
NoConn ~ 3000 4400
NoConn ~ 3000 4500
NoConn ~ 3000 4600
NoConn ~ 3000 4700
NoConn ~ 4600 4800
NoConn ~ 4600 4700
NoConn ~ 4600 4500
NoConn ~ 4600 4300
NoConn ~ 4600 4200
NoConn ~ 4600 4100
NoConn ~ 4600 3200
NoConn ~ 4600 3100
NoConn ~ 3700 2700
NoConn ~ 3600 2700
Text Label 5500 4250 2    50   ~ 0
GPIO
Text Label 5800 4250 0    50   ~ 0
GND
NoConn ~ 11400 3500
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 62187818
P 3650 2450
F 0 "#FLG0101" H 3650 2525 50  0001 C CNN
F 1 "PWR_FLAG" H 3650 2623 50  0000 C CNN
F 2 "" H 3650 2450 50  0001 C CNN
F 3 "~" H 3650 2450 50  0001 C CNN
	1    3650 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	3650 2450 3650 2550
Wire Wire Line
	3650 2550 3900 2550
Connection ~ 3900 2550
NoConn ~ 4100 5300
NoConn ~ 3900 5300
NoConn ~ 3600 5300
NoConn ~ 3500 5300
Wire Wire Line
	3400 5300 3400 5350
NoConn ~ 3800 5300
Wire Wire Line
	3900 2700 3900 2550
$Comp
L power:PWR_FLAG #FLG0102
U 1 1 6218C817
P 3200 5450
F 0 "#FLG0102" H 3200 5525 50  0001 C CNN
F 1 "PWR_FLAG" H 3200 5623 50  0000 C CNN
F 2 "" H 3200 5450 50  0001 C CNN
F 3 "~" H 3200 5450 50  0001 C CNN
	1    3200 5450
	-1   0    0    1   
$EndComp
Wire Wire Line
	3200 5450 3200 5350
Wire Wire Line
	3200 5350 3400 5350
Connection ~ 3400 5350
Wire Wire Line
	3400 5350 3400 5450
NoConn ~ 4600 4400
Wire Wire Line
	3400 5350 3700 5350
Wire Wire Line
	3700 5350 3700 5300
Wire Wire Line
	3700 5350 4000 5350
Wire Wire Line
	4000 5350 4000 5300
Connection ~ 3700 5350
Wire Wire Line
	4000 2700 4000 2550
Wire Wire Line
	4000 2550 3900 2550
Text Label 3900 2400 0    50   ~ 0
3V3
Wire Wire Line
	3900 2400 3900 2550
Wire Notes Line
	6650 1500 9450 1500
Wire Notes Line
	6650 2550 9450 2550
Wire Notes Line
	6650 6000 9450 6000
Text Label 7300 5550 2    50   ~ 0
3V3
Text Label 7300 5650 2    50   ~ 0
GPIO
Text Label 7300 5750 2    50   ~ 0
GND
Text Label 8500 5550 2    50   ~ 0
3V3
Text Label 8500 5650 2    50   ~ 0
GPIO
Text Label 8500 5750 2    50   ~ 0
GND
Wire Notes Line
	6650 3550 9450 3550
Wire Notes Line
	6650 4750 9450 4750
Wire Notes Line
	9450 1500 9450 6000
Wire Notes Line
	6650 6000 6650 1500
Text Notes 9500 3800 0    50   ~ 0
Bornier vissable 1Wire\n\n\n
Text Notes 9500 2650 0    50   ~ 0
Connecteur à clip I2C\n
Text Notes 9500 4950 0    50   ~ 0
Connecteur à clip 1Wire\n\n
Text Label 7300 5050 2    50   ~ 0
GPIO
Text Notes 9500 1650 0    50   ~ 0
Bornier vissable I2C\n\n
$Comp
L Connector:Raspberry_Pi_2_3 J10
U 1 1 62165500
P 3800 4000
F 0 "J10" H 3150 5250 50  0000 C CNN
F 1 "Raspberry_Pi_2_3" H 4400 5250 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical" H 3800 4000 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 3800 4000 50  0001 C CNN
	1    3800 4000
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x03_Odd_Even J20
U 1 1 621645E8
P 5600 5000
F 0 "J20" H 5650 5317 50  0000 C CNN
F 1 "Conn_GPIO" H 5650 5226 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical" H 5600 5000 50  0001 C CNN
F 3 "~" H 5600 5000 50  0001 C CNN
	1    5600 5000
	1    0    0    -1  
$EndComp
$Comp
L Connector:Screw_Terminal_01x04 J304
U 1 1 62293289
P 8700 1750
F 0 "J304" H 8780 1742 50  0000 L CNN
F 1 "Screw_Terminal_01x04" H 8780 1651 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_bornier-4_P5.08mm" H 8700 1750 50  0001 C CNN
F 3 "~" H 8700 1750 50  0001 C CNN
	1    8700 1750
	1    0    0    -1  
$EndComp
$Comp
L Connector:Screw_Terminal_01x04 J302
U 1 1 622929EF
P 8700 2250
F 0 "J302" H 8780 2242 50  0000 L CNN
F 1 "Screw_Terminal_01x04" H 8780 2151 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_bornier-4_P5.08mm" H 8700 2250 50  0001 C CNN
F 3 "~" H 8700 2250 50  0001 C CNN
	1    8700 2250
	1    0    0    -1  
$EndComp
Text Label 7300 1650 2    50   ~ 0
SCL
Text Label 7300 1750 2    50   ~ 0
SDA
Text Label 7300 2150 2    50   ~ 0
SCL
Text Label 7300 2250 2    50   ~ 0
SDA
Text Label 8500 1650 2    50   ~ 0
SCL
Text Label 8500 1750 2    50   ~ 0
SDA
Text Label 8500 2150 2    50   ~ 0
SCL
Text Label 8500 2250 2    50   ~ 0
SDA
Text Label 7300 1850 2    50   ~ 0
GND
Text Label 7300 1950 2    50   ~ 0
3V3
Text Label 7300 2350 2    50   ~ 0
GND
Text Label 7300 2450 2    50   ~ 0
3V3
Text Label 8500 2350 2    50   ~ 0
GND
Text Label 8500 2450 2    50   ~ 0
3V3
Text Label 8500 1850 2    50   ~ 0
GND
Text Label 8500 1950 2    50   ~ 0
3V3
$Comp
L Connector:Screw_Terminal_01x04 J303
U 1 1 6228CF9F
P 7500 1750
F 0 "J303" H 7580 1742 50  0000 L CNN
F 1 "Screw_Terminal_01x04" H 7580 1651 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_bornier-4_P5.08mm" H 7500 1750 50  0001 C CNN
F 3 "~" H 7500 1750 50  0001 C CNN
	1    7500 1750
	1    0    0    -1  
$EndComp
$Comp
L Connector:Screw_Terminal_01x04 J301
U 1 1 62292101
P 7500 2250
F 0 "J301" H 7580 2242 50  0000 L CNN
F 1 "Screw_Terminal_01x04" H 7580 2151 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_bornier-4_P5.08mm" H 7500 2250 50  0001 C CNN
F 3 "~" H 7500 2250 50  0001 C CNN
	1    7500 2250
	1    0    0    -1  
$EndComp
$Comp
L Connector:Screw_Terminal_01x03 J103
U 1 1 6228C086
P 7500 3850
F 0 "J103" H 7580 3892 50  0000 L CNN
F 1 "Screw_Terminal_01x03" H 7100 3550 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_bornier-3_P5.08mm" H 7500 3850 50  0001 C CNN
F 3 "~" H 7500 3850 50  0001 C CNN
	1    7500 3850
	1    0    0    -1  
$EndComp
$Comp
L Connector:Screw_Terminal_01x03 J104
U 1 1 622B682B
P 8700 3850
F 0 "J104" H 8780 3892 50  0000 L CNN
F 1 "Screw_Terminal_01x03" H 8300 3550 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_bornier-3_P5.08mm" H 8700 3850 50  0001 C CNN
F 3 "~" H 8700 3850 50  0001 C CNN
	1    8700 3850
	1    0    0    -1  
$EndComp
$Comp
L Connector:Screw_Terminal_01x03 J101
U 1 1 622B7368
P 7500 4450
F 0 "J101" H 7580 4492 50  0000 L CNN
F 1 "Screw_Terminal_01x03" H 7100 4250 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_bornier-3_P5.08mm" H 7500 4450 50  0001 C CNN
F 3 "~" H 7500 4450 50  0001 C CNN
	1    7500 4450
	1    0    0    -1  
$EndComp
$Comp
L Connector:Screw_Terminal_01x03 J102
U 1 1 622B7B53
P 8700 4450
F 0 "J102" H 8780 4492 50  0000 L CNN
F 1 "Screw_Terminal_01x03" H 8300 4250 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_bornier-3_P5.08mm" H 8700 4450 50  0001 C CNN
F 3 "~" H 8700 4450 50  0001 C CNN
	1    8700 4450
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x03 J3
U 1 1 622F2C14
P 7500 5050
F 0 "J3" H 7580 5092 50  0000 L CNN
F 1 "Conn_01x03" H 7580 5001 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 7500 5050 50  0001 C CNN
F 3 "~" H 7500 5050 50  0001 C CNN
	1    7500 5050
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x03 J1
U 1 1 622F4510
P 7500 5650
F 0 "J1" H 7580 5692 50  0000 L CNN
F 1 "Conn_01x03" H 7580 5601 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 7500 5650 50  0001 C CNN
F 3 "~" H 7500 5650 50  0001 C CNN
	1    7500 5650
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x03 J2
U 1 1 622F4D42
P 8700 5650
F 0 "J2" H 8780 5692 50  0000 L CNN
F 1 "Conn_01x03" H 8780 5601 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 8700 5650 50  0001 C CNN
F 3 "~" H 8700 5650 50  0001 C CNN
	1    8700 5650
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x03 J4
U 1 1 622F5415
P 8700 5050
F 0 "J4" H 8780 5092 50  0000 L CNN
F 1 "Conn_01x03" H 8780 5001 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 8700 5050 50  0001 C CNN
F 3 "~" H 8700 5050 50  0001 C CNN
	1    8700 5050
	1    0    0    -1  
$EndComp
$EndSCHEMATC

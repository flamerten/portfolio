---
date: 2026-01-06
slug:
description: Scripts for obfuscating strings in Arduino .ino files
tags:
  - Hardware/Security
  - Education/MSc-CEG
pin: false
---
# Arduino String Obfuscator
This assignment was done in partial fulfilment of [CEG5105 Cyber Security for Computer Systems](https://nusmods.com/courses/CEG5105/cyber-security-for-computer-systems#reviews). For the project, we were allowed to do any project related to Cyber Security. As a person interested in Embedded systems, I wanted to do a project related to securing embedded systems.

## The Problem
Its surprisingly easy to read strings from an Arduino if you have access to the bootloader. Using the `avrdude` utility, you can hexdump the contents of flash to a firmware hex file. After converting the hex file to binary, you can use the linux strings uitility to look for ASCII readable strings!

![[../../assets/arduino-string-obfuscator.png]]

This is also demonstrated in this repository [thomasbbrunner/arduino-reverse-engineering: Reverse engineering of an Arduino application](https://github.com/thomasbbrunner/arduino-reverse-engineering) where the author reverse-engineered the intent of the Arduino. This is a security issue, especially if your code has plenty of debug outputs.
## The Approach
There are a few ways to solve this. The easiest way would be to use `#ifdef` compilation directives to ensure that during deployment, you don't have any debug outputs. However, some applications must have strings. For example, if the application parses MQTT topics.

### One Time Pad

One possible way would be to use one time pad.

1. For each String `message` create a char array of the same length `cipher`
2. XOR the String with  char array and store it `new_msg = message ^ cipher`
3. When you need the string back, XOR the char array. `message = new_msg ^ cipher`

This means that 

- If you hex dump the firmware, you will see `new_msg` and `cipher` in the firmware
- You don't see `message`

However, this means that your memory has increased, and that if the adversary is smart enough, he will try to XOR any equal length character arrays and he will thus obtain `message`. Its makes reverse engineering harder, but its not very secure

### AES
Another option is to use AES encryption which requires a 128-bit key for all messages. This means that the only increase in memory usage is 128 bits. Even if the attacker gets access to the cipher, it is hard for him to know **which string** is the cipher. 

To make it even more challenging, we could store the key in an array of different size, and drop any unused bytes before decrypting the string to be used. This would make it slightly harder for the adversary to know how to parse the string **before** it can be used as the key.

We could also consider using hardware to improve security. For instance, storing the AES key in a secure element.

##  Conclusion
Even the AES method is not foolproof. An adversary could use [Ghidra](https://github.com/NationalSecurityAgency/ghidra) to trace the flash and figure out which string is being used the most or locate the decryption function. However that is much more challenging than dumping the binary and extracting ASCII readable strings.

Its important to note that when creating secure systems all systems are fallible. Its just the resources needed. Hence, we need to make assumptions on what the adversary can or cannot do. By implementing string obfuscation, we effectively raise the resources needed to reverse engineer our embedded system.

This project hence demonstrates a relatively simple way to secure an embedded system from adversaries from reading stored strings, which is the easiest way (in my humble opinion) of reverse engineering firmware. If I was working on a secure project, I would implement some CI/CD pipelines to ensure sensitive strings are not stored in plaintext.

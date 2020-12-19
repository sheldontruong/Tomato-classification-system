//**DELAY FUNCTION**//
//Author: Lokisv
//Date: 22/12/2018
//*****************************************
#include "stm32f10x.h"  
void Systick_enable()
{
	SysTick->CTRL = (1<<0);//enable systick
}
void delay_us(u32 time)
{
	SysTick->LOAD = time*10;
	SysTick->VAL = 0;
	while(!(SysTick->CTRL & (1<<16)));
}
void delay_ms(u32 time)
{
	SysTick->LOAD = time*10000;
	SysTick->VAL = 0;
	while(!(SysTick->CTRL & (1<<16)));
}

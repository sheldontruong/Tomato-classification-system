//**ĐỒ ÁN TÔT NGHIỆP**//
//Author: PHAT
//Date: 30/11/2019
//********************************************************
#include "stm32f10x.h"                  // Device header
#include "delay.h"
#include "header.h"
//-----------------------------------------------------------
const uint32_t wait = 2000;//fix this
char type1,type2,type3,type4;
uint32_t i=0,count1 = 0,count2 = 0,count3 = 0,count4 = 0;
uint8_t s1,s2,s3,s4,s5,cur_type;
uint8_t type_queue[10];
uint8_t pos[4];
uint32_t data;
uint8_t on,off;
//function for queue of tomato's type
//variable for queue
int queue_size = 9, front = 0, rear = 0;
void add_type(uint8_t new_type)
{
	int dem;
	for(dem = queue_size; dem>0;dem--)
	{
		type_queue[dem] = type_queue[dem-1];
	}
	type_queue[0] = new_type;
	if(rear < queue_size) rear++;
}
void rm_type(uint8_t pos)
{
	int dem;
	for(dem = pos ; dem < queue_size ; dem++)
	{
		type_queue[dem] = type_queue[dem+1];
	}
	type_queue[queue_size] = 0;
	if(rear>0) rear--;
}
uint8_t read_type()
{
	int type;
	data = ((GPIOB->IDR)&0x7000)>>12;
	if(data == 0) type = notomato;
	if(data == 1) type = red;
	if(data == 2) type = red_yellow;
	if(data == 3) type = green_yellow;
	if(data == 4) type = green;
	if(data == 5) type = corrupted;
	return type;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~//EXTI-8
void EXTI9_5_IRQHandler(void){
	if ((EXTI->PR&0x000100) != 0){
		EXTI->PR = (1<<8);
		if(read_type() != notomato) add_type(read_type());
		s1++;
	}
//~~~~~~~~~~~~~~~~~~~~~~~~~~//EXTI-9
	if ((EXTI->PR&0x000200) != 0){
		EXTI->PR = (1<<9);
		if(type_queue[pos[0]] == red) 
			{
				type1 = 1;
				rm_type(pos[0]);
			}
		else pos[0] = pos[0]+1;
		s2++;
	}
}
//~~~~~~~~~~~~~~~~~~~~~~~~~~//EXTI-10
void EXTI15_10_IRQHandler(void){
	if ((EXTI->PR&0x000400) != 0){
		EXTI->PR = (1<<10);
		s3++;
		if(type_queue[pos[1]] == red_yellow)
			{
				type2 = 1;
				rm_type(pos[1]);
				pos[0] = pos[0] - 1;
			}
		else pos[1] = pos[1]+1;
	}
//~~~~~~~~~~~~~~~~~~~~~~~~~//EXTI-11
	if ((EXTI->PR&0x000800) != 0){
		EXTI->PR = (1<<11);
		s4++;
		if(type_queue[pos[2]] == green_yellow)
			{
				type3 = 1;
				rm_type(pos[2]);
				pos[0] = pos[0] - 1;
				pos[1] = pos[1] - 1;
			}
		else pos[2] = pos[2]+1;
	}
//~~~~~~~~~~~~~~~~~~~~~~~~~//EXTI-12
	if ((EXTI->PR&0x001000) != 0){
		EXTI->PR = (1<<12);
		s5++;
		if(type_queue[pos[3]] == green)
			{
				type4 = 1;
				rm_type(pos[3]);
				pos[0] = pos[0] - 1;
				pos[1] = pos[1] - 1;
				pos[2] = pos[2] - 1;
			}
		else
			{
				rm_type(pos[3]);
				pos[0] = pos[0] - 1;
				pos[1] = pos[1] - 1;
				pos[2] = pos[2] - 1;
			}
	}
}

int main(void)
{
	Systick_enable();
	RCC->APB2ENR |= (1<<4)|(1<<3)|(1<<2)|(1<<0);//port c,port b, port a, afio
	//gpio, afio config
	//we should config AFIO->EXTICR here, but because i use all ext in port A so it's not nessecary anymore.
	GPIOB->CRH = (1<<0)|(2<<18)|(2<<22)|(2<<26);//b13,b12,b14: Input pulldown
	GPIOB->CRL = (2<<26)|(2<<30);
	GPIOA->CRL = (1<<4)|(1<<8)|(1<<12)|(1<<16)|(1<<20);//a1->a5: output push-pull, 10Mhz
	//exti config
	EXTI->IMR = (1<<8)|(1<<9)|(1<<10)|(1<<11)|(1<<12);//not masked the bit of 8->12
	EXTI->RTSR = 0;
	EXTI->FTSR = (1<<8)|(1<<9)|(1<<10)|(1<<11)|(1<<12);//falling edge on exti8->12
	NVIC_EnableIRQ(EXTI9_5_IRQn);
	NVIC_EnableIRQ(EXTI15_10_IRQn);
	
	while(1)
	{
		if(((GPIOB->IDR)&0x0040)>>6) {on = 1;off=0;}
		if(((GPIOB->IDR)&0x0080)>>7) {off = 1;on=0;}
		if(on)
		{
						if(type1 == 1) 
			{
				if(count1<wait) 	{ON_CY_1;count1++;}
				if(count1>=wait)	{OFF_CY_1;count1 = 0;type1 = 0;}
			}
			if(type2 == 1) 
			{
				if(count2<wait) 	{ON_CY_2;count2++;}
				if(count2>=wait)	{OFF_CY_2;count2 = 0;type2 = 0;}
			}
			if(type3 == 1) 
			{
				if(count3<wait) 	{ON_CY_3;count3++;}
				if(count3>=wait)	{OFF_CY_3;count3 = 0;type3 = 0;}
			}
			if(type4 == 1) 
			{
				if(count4<wait) 	{ON_CY_4;count4++;}
				if(count4>=wait)	{OFF_CY_4;count4 = 0;type4 = 0;}
			}
			ON_MO;
		}
		if(off) OFF_MO;
		ON_MO;
	}
	
}

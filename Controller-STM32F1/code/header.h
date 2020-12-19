#include "stm32f10x.h" 
//-----------------------------------------------------------
#define ON_CY_1 		GPIOA->ODR |= (1<<1)	
#define OFF_CY_1		GPIOA->ODR &= ~(1<<1)
#define ON_CY_2			GPIOA->ODR |= (1<<2)
#define OFF_CY_2		GPIOA->ODR &= ~(1<<2)
#define ON_CY_3			GPIOA->ODR |= (1<<3)
#define OFF_CY_3		GPIOA->ODR &= ~(1<<3)
#define ON_CY_4			GPIOA->ODR |= (1<<4)
#define OFF_CY_4		GPIOA->ODR &= ~(1<<4)
#define ON_MO 			GPIOB->ODR |= (1<<8)
#define OFF_MO			GPIOB->ODR &= ~(1<<8)
#define red 					1
#define red_yellow 		2
#define green_yellow 	3
#define green 				4
#define corrupted 		5
#define notomato			0
//-----------------------------------------------------------

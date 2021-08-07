/*
 *
 *  This source file is part of ELINA (ETH LIbrary for Numerical Analysis).
 *  ELINA is Copyright © 2019 Department of Computer Science, ETH Zurich
 *  This software is distributed under GNU Lesser General Public License Version 3.0.
 *  For more information, see the ELINA project website at:
 *  http://elina.ethz.ch
 *
 *  THE SOFTWARE IS PROVIDED "AS-IS" WITHOUT ANY WARRANTY OF ANY KIND, EITHER
 *  EXPRESS, IMPLIED OR STATUTORY, INCLUDING BUT NOT LIMITED TO ANY WARRANTY
 *  THAT THE SOFTWARE WILL CONFORM TO SPECIFICATIONS OR BE ERROR-FREE AND ANY
 *  IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE,
 *  TITLE, OR NON-INFRINGEMENT.  IN NO EVENT SHALL ETH ZURICH BE LIABLE FOR ANY     
 *  DAMAGES, INCLUDING BUT NOT LIMITED TO DIRECT, INDIRECT,
 *  SPECIAL OR CONSEQUENTIAL DAMAGES, ARISING OUT OF, RESULTING FROM, OR IN
 *  ANY WAY CONNECTED WITH THIS SOFTWARE (WHETHER OR NOT BASED UPON WARRANTY,
 *  CONTRACT, TORT OR OTHERWISE).
 *
 */



/* ************************************************************************* */
/* elina_scalar.h: scalars */
/* ************************************************************************* */

#ifndef _ELINA_SCALAR_H_
#define _ELINA_SCALAR_H_

#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


#include "elina_config.h"

#ifdef __cplusplus
extern "C" {
#endif


/* ********************************************************************** */
/* I. Datatypes  */
/* ********************************************************************** */

typedef enum elina_scalar_discr_t {
  ELINA_SCALAR_DOUBLE, /* double-precision floating-point number */
} elina_scalar_discr_t;

typedef struct elina_scalar_t {
  elina_scalar_discr_t discr;
  union {
    double dbl;
    
  } val;
} elina_scalar_t;

/* ********************************************************************** */
/* II. Operations  */
/* ********************************************************************** */

/* ====================================================================== */
/* Basics */
/* ====================================================================== */

elina_scalar_t* elina_scalar_alloc(void);
  /* Allocates a scalar, of default type DOUBLE (the most economical) */
void elina_scalar_free(elina_scalar_t* scalar);
  /* Free a scalar */
void elina_scalar_reinit(elina_scalar_t* scalar, elina_scalar_discr_t d);
  /* Change the type of an already allocated scalar
     (mainly for internal use */

void elina_scalar_print(elina_scalar_t* a);
void elina_scalar_fprint(FILE* stream, elina_scalar_t* a);
  /* Printing */

extern int elina_scalar_print_prec;
  /* Number of significant digits to print for floating-point numbers.
     Defaults to 20.
   */


void elina_scalar_swap(elina_scalar_t* a, elina_scalar_t* b);
  /* Exchange */

/* ====================================================================== */
/* Assignments */
/* ====================================================================== */

void elina_scalar_set(elina_scalar_t* scalar, elina_scalar_t* scalar2);
  /* Assignment */
void elina_scalar_set_int(elina_scalar_t* scalar, long int i);
void elina_scalar_set_frac(elina_scalar_t* scalar, long int i, unsigned long int j);
  /* Change the type of scalar  and initialize it resp. with
     
     - integer i
     - rational i/j, assuming j!=0
  */
void elina_scalar_set_double(elina_scalar_t* scalar, double k);
  /* Change the type of scalar to DOUBLE and initialize it with k. */
void elina_scalar_set_infty(elina_scalar_t* scalar, int sgn);
  /* Assignment to sgn*infty. Keep the type of the scalar.
     If sgn == 0, set to zero. */

/* ====================================================================== */
/* Combined allocation and assignment */
/* ====================================================================== */

elina_scalar_t* elina_scalar_alloc_set(elina_scalar_t* scalar2);

elina_scalar_t* elina_scalar_alloc_set_double(double k);
  /* Allocate an DOUBLE scalar and initialize it with k. */

/* ====================================================================== */
/* Conversions */
/* ====================================================================== */

/* For the two next functions, the returned value is zero if conversion is
   exact, positive if the result is greater, negative if it is lower. */



/* ====================================================================== */
/* Tests */
/* ====================================================================== */

int elina_scalar_infty(elina_scalar_t* scalar);
  /* -1:-infty, 0:finite; 1:+infty */
int elina_scalar_cmp(elina_scalar_t* a, elina_scalar_t* b);
int elina_scalar_cmp_int(elina_scalar_t* a, int b);
  /* Exact comparison between two scalars (resp. a scalar and an integer)
     -1: a is less than b
     0: a is equal to b
     1: a is greater than b
  */
bool elina_scalar_equal(elina_scalar_t* a, elina_scalar_t* b);
bool elina_scalar_equal_int(elina_scalar_t* a, int b);
  /* Exact Equality test */
int elina_scalar_sgn(elina_scalar_t* a);
  /* -1: negative, 0: null, +1: positive  */

/* ====================================================================== */
/* Other operations */
/* ====================================================================== */

void elina_scalar_neg(elina_scalar_t* a, elina_scalar_t* b);
  /* Negation */
void elina_scalar_inv(elina_scalar_t* a, elina_scalar_t* b);
  /* Inversion. Not exact for floating-point type */

long elina_scalar_hash(elina_scalar_t* a);
  /* Return an hash code (for instance for OCaml interface) */

/* ********************************************************************** */
/* III. FOR INTERNAL USE ONLY */
/* ********************************************************************** */

static inline
void elina_scalar_init(elina_scalar_t* scalar, elina_scalar_discr_t d)
{
  scalar->discr = d;
  switch(d){
  case ELINA_SCALAR_DOUBLE:
    scalar->val.dbl = 0.0;
    break;
  }
}
static inline
void elina_scalar_clear(elina_scalar_t* scalar)
{
  switch(scalar->discr){
  case ELINA_SCALAR_DOUBLE:
    break;
  }
}




#ifdef __cplusplus
}
#endif

#endif

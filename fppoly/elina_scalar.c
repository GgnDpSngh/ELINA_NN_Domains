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
/* elina_scalar.c: coefficients and intervals */
/* ************************************************************************* */


#include <stdlib.h>
#include <math.h>
#include <limits.h>
#include <assert.h>
#include "elina_scalar.h"

/* ====================================================================== */
/* Basics */
/* ====================================================================== */

elina_scalar_t* elina_scalar_alloc()
{
  elina_scalar_t* scalar = malloc(sizeof(elina_scalar_t));
  scalar->discr = ELINA_SCALAR_DOUBLE;
  scalar->val.dbl = 0.0;
  return scalar;
}

void elina_scalar_reinit(elina_scalar_t* scalar, elina_scalar_discr_t d)
{ 
  if (scalar->discr != d){
    elina_scalar_clear(scalar);
    elina_scalar_init(scalar,d);
  }
}

void elina_scalar_free(elina_scalar_t* scalar)
{
  elina_scalar_clear(scalar);
  free(scalar);
}

int elina_scalar_print_prec = 20;

void elina_scalar_fprint(FILE* stream, elina_scalar_t* a)
{
  int flag;

  flag = elina_scalar_infty(a);
  if (flag){
    fprintf(stream, flag>0 ? "+oo" : "-oo");
  }
  else {
    switch(a->discr){
    case ELINA_SCALAR_DOUBLE:
      fprintf(stream,"%.*g",elina_scalar_print_prec,a->val.dbl + 0.0);
      break;
    
    default: 
      abort();
    }
  } 
}

/* ====================================================================== */
/* Combined allocation and assignments */
/* ====================================================================== */

elina_scalar_t* elina_scalar_alloc_set(elina_scalar_t* b)
{
  elina_scalar_t* a = malloc(sizeof(elina_scalar_t));
  a->discr = b->discr;
  switch(b->discr){
  case ELINA_SCALAR_DOUBLE:
    a->val.dbl = b->val.dbl;
    break;
  
  default: 
    abort();
  }
  return a;
}

elina_scalar_t* elina_scalar_alloc_set_double(double k)
{
  elina_scalar_t* a = malloc(sizeof(elina_scalar_t));
  a->discr = ELINA_SCALAR_DOUBLE;
  a->val.dbl = k;
  return a;
}

/* ====================================================================== */
/* Assignments */
/* ====================================================================== */

void elina_scalar_set(elina_scalar_t* a, elina_scalar_t* b)
{
  
  if (a==b) return;
  elina_scalar_reinit(a,b->discr);
  switch(b->discr){
  case ELINA_SCALAR_DOUBLE:
    a->val.dbl = b->val.dbl;
    break;
  
  default: 
    abort();
  }
}


void elina_scalar_set_double(elina_scalar_t* scalar, double k)
  { elina_scalar_reinit(scalar,ELINA_SCALAR_DOUBLE); scalar->val.dbl = k; }
void elina_scalar_set_infty(elina_scalar_t* scalar, int sgn)
{
  switch(scalar->discr){
  
  case ELINA_SCALAR_DOUBLE:
    scalar->val.dbl = sgn>0 ? (double)1.0/(double)0.0 : (sgn < 0 ? -(double)1.0/(double)0.0 : 0.0);
    break;
  
  default:
    abort();
  }
}

/* ====================================================================== */
/* Conversions */
/* ====================================================================== */




int elina_double_set_scalar(double* k, elina_scalar_t* scalar)
{
  switch(scalar->discr){
  
  case ELINA_SCALAR_DOUBLE:
    *k = scalar->val.dbl;
    return 0;
  
  default:
    abort();
  }


}

/* ====================================================================== */
/* Tests */
/* ====================================================================== */

int elina_scalar_infty(elina_scalar_t* scalar)
{
  switch(scalar->discr){
  
  case ELINA_SCALAR_DOUBLE:
    return 
      scalar->val.dbl==(double)1.0/(double)0.0 ?
      1 :
      ( scalar->val.dbl==-(double)1.0/(double)0.0 ?
	-1 :
	0);
  
  default:
    abort();
  }
}

int elina_scalar_cmp(elina_scalar_t* a, elina_scalar_t* b)
{
  int s1 = elina_scalar_infty(a);
  int s2 = elina_scalar_infty(b);
  
  if (s1>s2)
    return 1;
  else if (s1<s2)
    return -1;
  else if (s1!=0)
    return 0;
  switch (a->discr){
    
    case ELINA_SCALAR_DOUBLE:
      return 
	a->val.dbl > b->val.dbl ?
	1 :
      ( a->val.dbl < b->val.dbl ?
	-1 :
	0);
    
    default:
      abort();
    }
 
}


int elina_scalar_cmp_int(elina_scalar_t* a, int b)
{
  int s1 = elina_scalar_infty(a);
  
  if (s1>0)
    return 1;
  else if (s1<0)
    return -1;
  else {
    switch (a->discr){
    case ELINA_SCALAR_DOUBLE:
      return a->val.dbl > b ? 1 : (a->val.dbl < b ? (-1) : 0);
    
    default:
      abort();
    }
  }
}
bool elina_scalar_equal(elina_scalar_t* a, elina_scalar_t* b)
{
  int s1 = elina_scalar_infty(a);
  int s2 = elina_scalar_infty(b);
  
  if (s1!=s2)
    return false;
  else if (s1!=0)
    return true;
  else if (a->discr == b->discr) {
    switch (a->discr){
    
    case ELINA_SCALAR_DOUBLE: return a->val.dbl == b->val.dbl;
    
    default:               abort();
    }
  }
  else return elina_scalar_cmp(a,b)==0;
}
bool elina_scalar_equal_int(elina_scalar_t* a, int b)
{
  int s1 = elina_scalar_infty(a);
  
  if (s1!=0)
    return false;
  else {
    switch (a->discr){
    case ELINA_SCALAR_DOUBLE:  return a->val.dbl == b;
    
    default:                abort();
    }
  }
}

int elina_scalar_sgn(elina_scalar_t* a)
{
  int res;
  res = elina_scalar_infty(a);
  if (!res) {
    switch (a->discr){
    
    case ELINA_SCALAR_DOUBLE: res = a->val.dbl > 0.0 ? 1 : (a->val.dbl == 0.0 ? 0 : (-1)); break;
    
    default:               abort();
    }
  }
  return res > 0 ? 1 : res < 0 ? -1 : 0;
}

/* ====================================================================== */
/* Other operations */
/* ====================================================================== */

void elina_scalar_neg(elina_scalar_t* a, elina_scalar_t* b)
{
  elina_scalar_reinit(a,b->discr);
  switch(b->discr){
  
  case ELINA_SCALAR_DOUBLE:
    a->val.dbl = -b->val.dbl;
    break;
  
  default:
    abort();
  }
}
void elina_scalar_inv(elina_scalar_t* a, elina_scalar_t* b)
{
  elina_scalar_reinit(a,b->discr);
  switch(b->discr){
  
  case ELINA_SCALAR_DOUBLE:
    a->val.dbl = 1.0/b->val.dbl;
    break;
  
  default:
    abort();
  }
}

long elina_scalar_hash(elina_scalar_t* a)
{
  int infty = elina_scalar_infty(a);
  if (infty<0) return LONG_MIN;
  else if (infty>0) return LONG_MAX;
  else {
    switch (a->discr){
    
    case ELINA_SCALAR_DOUBLE:
      return (int)(a->val.dbl);
    
    default:
      abort();
    }
  }
}

void elina_scalar_print(elina_scalar_t* a)
{ elina_scalar_fprint(stdout,a); }

void elina_scalar_swap(elina_scalar_t* a, elina_scalar_t* b){ elina_scalar_t t = *a; *a = *b; *b = t; }

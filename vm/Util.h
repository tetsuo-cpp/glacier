#ifndef GLACIERVM_UTIL_H
#define GLACIERVM_UTIL_H

#define GLC_DECL_RET int ret = 0

#define GLC_RET(a)                                                             \
  do {                                                                         \
    int __ret;                                                                 \
    if ((__ret = (a)) != 0)                                                    \
      return (__ret);                                                          \
  } while (0)

#define GLC_ERR(a)                                                             \
  do {                                                                         \
    if ((ret = (a)) != 0)                                                      \
      goto err;                                                                \
  } while (0)

#define GLC_UNUSED(a) (void)(a)

#define GLC_OK 0
#define GLC_ERROR -1
#define GLC_INVALID_OP -2
#define GLC_OUT_OF_BUFFER -3
#define GLC_STACK_OVERFLOW -4

#endif // GLACIERVM_UTIL_H
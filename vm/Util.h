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

#ifdef LOG_DBG
#define GLC_LOG_DBG(format, ...) printf(format, ##__VA_ARGS__)
#else
#define GLC_LOG_DBG(format, ...)                                               \
  do {                                                                         \
  } while (0)
#endif

#define GLC_LOG_ERR(format, ...) fprintf(stderr, format, ##__VA_ARGS__)

static inline const char *glacierUtilErrorToString(int error) {
  switch (error) {
  case GLC_OK:
    return "GLC_OK";
  case GLC_ERROR:
    return "GLC_ERROR";
  case GLC_INVALID_OP:
    return "GLC_INVALID_OP";
  case GLC_OUT_OF_BUFFER:
    return "GLC_OUT_OF_BUFFER";
  case GLC_STACK_OVERFLOW:
    return "GLC_STACK_OVERFLOW";
  default:
    return "UNKNOWN";
  }
}

#endif // GLACIERVM_UTIL_H

#ifndef GLACIERVM_STACK_H
#define GLACIERVM_STACK_H

#define MAX_STACK_SIZE 1024
#define MAX_FRAME_BINDINGS 1024

// Maybe make this a union and type pun for other types.
typedef struct {
  int value;
} GlacierStackFrame;

typedef struct {
  GlacierStackFrame data[MAX_STACK_SIZE];
  int stackPointer;
} GlacierStack;

void glacierStackInit(GlacierStack *stack);
int glacierStackPush(GlacierStack *stack, int value);
int glacierStackTop(GlacierStack *stack, int *value);
int glacierStackPop(GlacierStack *stack, int *value);

typedef struct {
  int bindings[MAX_FRAME_BINDINGS];
  int numBindings;
} GlacierCallStackFrame;

typedef struct {
  GlacierCallStackFrame frames[MAX_STACK_SIZE];
  int stackPointer;
} GlacierCallStack;

void glacierCallStackInit(GlacierCallStack *stack);
int glacierCallStackPush(GlacierCallStack *stack);
int glacierCallStackPop(GlacierCallStack *stack);
int glacierCallStackGet(GlacierCallStack *stack, int id, int *value);
int glacierCallStackSet(GlacierCallStack *stack, int id, int value);
void glacierCallStackFrameInit(GlacierCallStackFrame *frame);

#endif // GLACIERVM_STACK_H

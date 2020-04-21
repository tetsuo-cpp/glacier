# Glacier
This is a toy statically typed object oriented programming language that I'm working on to consolidate what I've learnt about compilers so far.

There are two components:
* A compiler written in Python that parses Glacier source code and emits a custom bytecode format.
* A stack-based virtual machine written in C that executes this bytecode.
## Build
Setup a Python virtual environment for running the Glacier compiler.
```
$ bash setup_env.sh
```
The Glacier VM requires dependencies such as the Boehm-Demers-Weiser Garbage Collector so they need to be pulled in as submodules before invoking the CMake build.
```
$ git submodule init
$ cmake . && make
```
## Usage
```
$ source .ve/bin/activate
$ ./glacierc <glacier_source> -o <bytecode>
$ ./glaciervm <bytecode>
```
Run unit tests.
```
$ bash unit_test.sh
```
Run system tests.
```
$ bash system_test_all.sh
```
## Hello World!
```
fn main() -> void {
  print("Hello World!");
}
```
## Features
This is not an exhaustive list. The examples under the `system_tests/` directory are the source of truth for what features Glacier supports at any given time.
### Control flow
Glacier supports conditionals and loops.
```
fn main() -> void {
  // Print numbers from 0-9.
  let count = 0;
  while (count < 10) {
    if (counter == 5) {
      print("five");
    } else {
      print(count);
    }
    count = count + 1;
  }
}
```
### Types and data structures
Glacier supports a range of built in types.
* Integer.
* String.
* Vector.
* Hashmap.
### Static typing
Glacier is a statically typed language meaning that certain classes of bugs can be caught at compile time.
```
fn bar(int num) -> int {
  ...
}

fn main() -> void {
  let foo = "Hello World!";
  bar(foo); // Compilation error. We tried to pass a string into a function taking an int arg.
}
```
### Type inference
Glacier infers type declarations where possible making code less verbose.
```
fn createMap(int num) -> map<int, string> {
  ...
}

fn main() -> void {
  let integerType = 1;
  let stringType = "Hello World!";
  let mapType = createMap(10);
}
```
### Structs
Glacier supports bundling related data types together and binding methods to them. These types can be used in conjunction with built in data structures such as `vector` and `map`.
```
struct Doubler {
  int num;
  fn double() -> int {
    this.num = this.num * 2;
    return this.num;
  }
};

fn main() -> void {
  let doubler = new Doubler(2);
  print(doubler.num); // 2
  doubler.double();
  print(doubler.num); // 4
  let vectorOfDoublers = [doubler, new Doubler(10)]<Doubler>;
}
```
Glacier also supports default arguments for struct constructors.
```
struct Person {
  string name = "Alex";
  int age = 24;
};

fn main() -> void {
  let person1 = new Person(); // Alex, 24
  let person2 = new Person("Michelle"); // Michelle, 24
  let person3 = new Person("Michelle", 26); // Michelle, 26
}
```
### Disassembler
Glacier also provides a bytecode disassembler to debug the compiler and VM.
```
$ ./glacierd system_tests/example_1/example_1.bc
STRUCT_DEF (0)
  type_id: 2
  member_id_len: 2
    member_id_0: 1
    member_id_1: 0
FUNCTION_JMP (5)
  function_id: 1
  offset: 0
FUNCTION_JMP (8)
  function_id: 2
  offset: 10
FUNCTION_JMP (11)
  function_id: 0
  offset: 20
...
```
## Glacier DSL
The definitions of what ops exist in the GlacierVM are described by a Python DSL in `glacierdsl`. Running `glacierdsl` will generate:
* A C header for the VM containing `#define`s for each opcode (`Ops.h`).
* A Python file for the compiler containing serialisation classes for writing bytecode for each op (`compiler/ops.py`).
* A Python file for the disassembler containing a function to print an op from bytecode in human readable form (`disassembler/ops.py`).
## TODO
* Make object stack resizeable.
* More sensible bytecode format (at the moment all arguments are 1 byte).
* More tests around static typing.
* Reduce technical debt and general hackiness.
* Improve compiler errors and diagnostics.

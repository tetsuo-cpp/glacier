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
The Glacier VM requires the Boehm-Demers-Weiser Garbage Collector so this needs to be pulled in as a submodule before invoking the CMake build.
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
fn main() -> int {
  print("Hello World!");
  return 0;
}
```
## Features
This is not an exhaustive list. The examples under the `system_tests/` directory are the source of truth for what features Glacier supports at any given time.
### Control flow
Glacier supports conditionals and loops.
```
fn main() -> int {
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
  return 0;
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

fn main() -> int {
  let foo = "Hello World!";
  bar(foo); // Compilation error. We tried to pass a string into a function taking an int arg.
  return 0;
}
```
### Type inference
Glacier infers type declarations where possible making code less verbose.
```
fn createMap(int num) -> map<int, string> {
  ...
}

fn main() -> int {
  let integerType = 1;
  let stringType = "Hello World!";
  let mapType = createMap(10);
  return 0;
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

fn main() -> int {
  let doubler = new Doubler(2);
  print(doubler.num); // 2
  doubler.double();
  print(doubler.num); // 4
  let vectorOfDoublers = [doubler, new Doubler(10)]<Doubler>;
  return 0;
}
```
Glacier also supports default arguments for struct constructors.
```
struct Person {
  string name = "Alex";
  int age = 24;
};

fn main() -> int {
  let person1 = new Person(); // Alex, 24
  let person2 = new Person("Michelle"); // Michelle, 24
  let person3 = new Person("Michelle", 26); // Michelle, 26
  return 0;
}
```
### Disassembler
Glacier also provides a bytecode disassembler to debug the compiler and VM.
```
$ ./glacierd system_tests/example_1/example_1.bc
STRUCT_DEF (0)
  TypeId: 2
  NumMembers: 2
    MemberTypeId0: 1
    MemberTypeId1: 0
FUNCTION_JMP (5)
  TypeId: 1
  Offset: 0
FUNCTION_JMP (8)
  TypeId: 2
  Offset: 9
FUNCTION_JMP (11)
  TypeId: 0
  Offset: 18
...
```
## TODO
* Make object stack resizeable.
* Built-in functions (push, insert, etc).
* More sensible bytecode format (at the moment all arguments are 1 byte).
* Generate bytecode definitions in C and Python from a definition language.
* More tests around static typing.
* Reduce technical debt and general hackiness.
* Improve compiler errors and diagnostics.

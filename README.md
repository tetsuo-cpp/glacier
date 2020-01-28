# Glacier
This is a toy statically typed object oriented programming language that I'm working on to consolidate what I've learnt about compilers so far.

There are two components:
* A compiler written in Python that parses Glacier source code and emits a custom bytecode format.
* A stack-based virtual machine written in C that executes this bytecode.
## Definition
I'll be making this up as I go along but here are some ideas.
```
struct Person {
  string occupation;
  string name = "Alex";
  int age = 24;

  fn growOlder() -> int {
    this.age = this.age + 1;
    return this.age;
  }
};

fn printNum(int num) -> void {
   print(num);
}

fn main() -> int {
  // Basic flow control.
  let num = 1;

  // Prints 1 => 10 with while loop.
  while (num <= 10) {
    print(num);
    num = num + 1;
  }

  // Conditionals.
  if (num == 10) {
    print("We should see this.");
  } else {
    print("But not this!");
  }

  printNum(num); // 10
  printNum(1); // 1
  printNum("hello world"); // Compiler error.

  // Using structs.
  // Provide all arguments.
  let tom = Person("manager", "Tom", 30);

  // Or use some of the defaults.
  let alex = Person("dev");
  print(alex.name); // "Alex"
  while (alex.age < 100) {
    alex.growOlder();
  }

  // Vector and map usage.
  let vec = [8, 2]<int>;
  print(vec[0]); // 8
  push(vec, 6);
  push(vec, "foo"); // Compiler error.
  pop(vec);

  let map = { "foo": 21, "bar": 9 }<string, int>;
  print(map["foo"]); // 21
  insert(map, "foobar", 3);
  insert(map, 1, 2); // Compiler error.

  return 0;
}
```
## TODO
* Default arguments in constructors.
* Integrate Boehm GC.
* Make object stack resizeable.
* Vectors.
* Maps.
* Built-in functions (push, insert, etc).
* More sensible bytecode format (at the moment all arguments are 1 byte).
* Generate bytecode definitions in C and Python from a definition language.
* More tests around static typing.
* Reduce technical debt and general hackiness.
* Improve compiler errors and diagnostics.

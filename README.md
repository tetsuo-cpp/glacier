# Glacier
This is a toy object oriented programming language that I'm working on to consolidate what I've learnt about compilers so far. I plan to compile down to a custom bytecode format that I'll write a VM for (in C).
## Definition
I'll be making this up as I go along but here are some ideas.
```
struct Foo {
  string name = "alex";
  int number = 10;

  fn getName() -> string {
    return name;
  };
};

fn main() -> int {
  let foo = Foo("foo");
  print(foo.getName()); // alex
  print(foo.name); // alex
  print(foo.number); // 10
  let x = 1;
  let y = x + 1;
  if (x == 2) {
    print(x);
  }
  print(y); // 2
  let bar = Foo("bar", 20);
  print(bar.getName()); // bar
  print(bar.name); // bar
  print(bar.number); // 20
};
```
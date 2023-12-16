#include <stdio.h>

extern "C" {
  void prTest(char* name)
  {
    printf("Everythin works fine, %s\n", name);
  }
}

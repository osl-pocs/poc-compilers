import llvm.ee as le
import llvm.core as lc

int_type   = lc.Type.int()
float_type = lc.Type.double()
void_type  = lc.Type.void()

def func(name, module, rettype, argtypes):
    func_type   = lc.Type.function(rettype, argtypes, False)
    lfunc       = lc.Function.new(module, func_type, name)
    entry_block = lfunc.append_basic_block("entry")
    builder     = lc.Builder.new(entry_block)
    return (lfunc, builder)


# When we call Python's __repr__ function it will print out the LLVM IR
# to the module.
mod = lc.Module.new('mymodule')
print(mod)

(fn, builder) = func('main', mod, int_type, [])
print(fn)

value = lc.Constant.int(int_type, 42)
block = builder.ret(value)
print(mod)


print(mod.to_native_assembly())

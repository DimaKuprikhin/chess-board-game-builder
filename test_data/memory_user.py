def good_memory_user():
  # Memory limit: 128MB, here we create a list that consumes 80MB
  # (56B for list + 8B for each element).
  list_size = (80 * 1024 * 1024 - 56) // 8
  list_ = [0] * list_size
  return list_[2]


def bad_memory_user():
  # Create a list that consumes all the memory and get MemoryError.
  list_size = (128 * 1024 * 1024 - 56) // 8
  list_ = [0] * list_size
  return list_[2]

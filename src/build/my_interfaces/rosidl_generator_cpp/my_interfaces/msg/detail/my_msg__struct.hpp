// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from my_interfaces:msg/MyMsg.idl
// generated code does not contain a copyright notice

#ifndef MY_INTERFACES__MSG__DETAIL__MY_MSG__STRUCT_HPP_
#define MY_INTERFACES__MSG__DETAIL__MY_MSG__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__my_interfaces__msg__MyMsg __attribute__((deprecated))
#else
# define DEPRECATED__my_interfaces__msg__MyMsg __declspec(deprecated)
#endif

namespace my_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MyMsg_
{
  using Type = MyMsg_<ContainerAllocator>;

  explicit MyMsg_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->a = 0l;
      this->b = 0.0f;
    }
  }

  explicit MyMsg_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->a = 0l;
      this->b = 0.0f;
    }
  }

  // field types and members
  using _a_type =
    int32_t;
  _a_type a;
  using _b_type =
    float;
  _b_type b;

  // setters for named parameter idiom
  Type & set__a(
    const int32_t & _arg)
  {
    this->a = _arg;
    return *this;
  }
  Type & set__b(
    const float & _arg)
  {
    this->b = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    my_interfaces::msg::MyMsg_<ContainerAllocator> *;
  using ConstRawPtr =
    const my_interfaces::msg::MyMsg_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<my_interfaces::msg::MyMsg_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<my_interfaces::msg::MyMsg_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      my_interfaces::msg::MyMsg_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<my_interfaces::msg::MyMsg_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      my_interfaces::msg::MyMsg_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<my_interfaces::msg::MyMsg_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<my_interfaces::msg::MyMsg_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<my_interfaces::msg::MyMsg_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__my_interfaces__msg__MyMsg
    std::shared_ptr<my_interfaces::msg::MyMsg_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__my_interfaces__msg__MyMsg
    std::shared_ptr<my_interfaces::msg::MyMsg_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MyMsg_ & other) const
  {
    if (this->a != other.a) {
      return false;
    }
    if (this->b != other.b) {
      return false;
    }
    return true;
  }
  bool operator!=(const MyMsg_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MyMsg_

// alias to use template instance with default allocator
using MyMsg =
  my_interfaces::msg::MyMsg_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace my_interfaces

#endif  // MY_INTERFACES__MSG__DETAIL__MY_MSG__STRUCT_HPP_

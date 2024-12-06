// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_interfaces:msg/MyMsg.idl
// generated code does not contain a copyright notice

#ifndef MY_INTERFACES__MSG__DETAIL__MY_MSG__BUILDER_HPP_
#define MY_INTERFACES__MSG__DETAIL__MY_MSG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_interfaces/msg/detail/my_msg__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_interfaces
{

namespace msg
{

namespace builder
{

class Init_MyMsg_b
{
public:
  explicit Init_MyMsg_b(::my_interfaces::msg::MyMsg & msg)
  : msg_(msg)
  {}
  ::my_interfaces::msg::MyMsg b(::my_interfaces::msg::MyMsg::_b_type arg)
  {
    msg_.b = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_interfaces::msg::MyMsg msg_;
};

class Init_MyMsg_a
{
public:
  Init_MyMsg_a()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MyMsg_b a(::my_interfaces::msg::MyMsg::_a_type arg)
  {
    msg_.a = std::move(arg);
    return Init_MyMsg_b(msg_);
  }

private:
  ::my_interfaces::msg::MyMsg msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_interfaces::msg::MyMsg>()
{
  return my_interfaces::msg::builder::Init_MyMsg_a();
}

}  // namespace my_interfaces

#endif  // MY_INTERFACES__MSG__DETAIL__MY_MSG__BUILDER_HPP_

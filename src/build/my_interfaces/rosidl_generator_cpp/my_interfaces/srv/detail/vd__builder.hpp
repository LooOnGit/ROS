// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_interfaces:srv/Vd.idl
// generated code does not contain a copyright notice

#ifndef MY_INTERFACES__SRV__DETAIL__VD__BUILDER_HPP_
#define MY_INTERFACES__SRV__DETAIL__VD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_interfaces/srv/detail/vd__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_interfaces
{

namespace srv
{

namespace builder
{

class Init_Vd_Request_theta
{
public:
  explicit Init_Vd_Request_theta(::my_interfaces::srv::Vd_Request & msg)
  : msg_(msg)
  {}
  ::my_interfaces::srv::Vd_Request theta(::my_interfaces::srv::Vd_Request::_theta_type arg)
  {
    msg_.theta = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_interfaces::srv::Vd_Request msg_;
};

class Init_Vd_Request_y
{
public:
  explicit Init_Vd_Request_y(::my_interfaces::srv::Vd_Request & msg)
  : msg_(msg)
  {}
  Init_Vd_Request_theta y(::my_interfaces::srv::Vd_Request::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Vd_Request_theta(msg_);
  }

private:
  ::my_interfaces::srv::Vd_Request msg_;
};

class Init_Vd_Request_x
{
public:
  Init_Vd_Request_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Vd_Request_y x(::my_interfaces::srv::Vd_Request::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Vd_Request_y(msg_);
  }

private:
  ::my_interfaces::srv::Vd_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_interfaces::srv::Vd_Request>()
{
  return my_interfaces::srv::builder::Init_Vd_Request_x();
}

}  // namespace my_interfaces


namespace my_interfaces
{

namespace srv
{

namespace builder
{

class Init_Vd_Response_sum
{
public:
  Init_Vd_Response_sum()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::my_interfaces::srv::Vd_Response sum(::my_interfaces::srv::Vd_Response::_sum_type arg)
  {
    msg_.sum = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_interfaces::srv::Vd_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_interfaces::srv::Vd_Response>()
{
  return my_interfaces::srv::builder::Init_Vd_Response_sum();
}

}  // namespace my_interfaces

#endif  // MY_INTERFACES__SRV__DETAIL__VD__BUILDER_HPP_

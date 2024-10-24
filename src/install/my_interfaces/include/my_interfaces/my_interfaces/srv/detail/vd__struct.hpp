// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from my_interfaces:srv/Vd.idl
// generated code does not contain a copyright notice

#ifndef MY_INTERFACES__SRV__DETAIL__VD__STRUCT_HPP_
#define MY_INTERFACES__SRV__DETAIL__VD__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__my_interfaces__srv__Vd_Request __attribute__((deprecated))
#else
# define DEPRECATED__my_interfaces__srv__Vd_Request __declspec(deprecated)
#endif

namespace my_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Vd_Request_
{
  using Type = Vd_Request_<ContainerAllocator>;

  explicit Vd_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0f;
      this->y = 0.0f;
      this->theta = 0.0f;
    }
  }

  explicit Vd_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0f;
      this->y = 0.0f;
      this->theta = 0.0f;
    }
  }

  // field types and members
  using _x_type =
    float;
  _x_type x;
  using _y_type =
    float;
  _y_type y;
  using _theta_type =
    float;
  _theta_type theta;

  // setters for named parameter idiom
  Type & set__x(
    const float & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const float & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__theta(
    const float & _arg)
  {
    this->theta = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    my_interfaces::srv::Vd_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const my_interfaces::srv::Vd_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<my_interfaces::srv::Vd_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<my_interfaces::srv::Vd_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      my_interfaces::srv::Vd_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<my_interfaces::srv::Vd_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      my_interfaces::srv::Vd_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<my_interfaces::srv::Vd_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<my_interfaces::srv::Vd_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<my_interfaces::srv::Vd_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__my_interfaces__srv__Vd_Request
    std::shared_ptr<my_interfaces::srv::Vd_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__my_interfaces__srv__Vd_Request
    std::shared_ptr<my_interfaces::srv::Vd_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Vd_Request_ & other) const
  {
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->theta != other.theta) {
      return false;
    }
    return true;
  }
  bool operator!=(const Vd_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Vd_Request_

// alias to use template instance with default allocator
using Vd_Request =
  my_interfaces::srv::Vd_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace my_interfaces


#ifndef _WIN32
# define DEPRECATED__my_interfaces__srv__Vd_Response __attribute__((deprecated))
#else
# define DEPRECATED__my_interfaces__srv__Vd_Response __declspec(deprecated)
#endif

namespace my_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Vd_Response_
{
  using Type = Vd_Response_<ContainerAllocator>;

  explicit Vd_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->sum = 0.0f;
    }
  }

  explicit Vd_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->sum = 0.0f;
    }
  }

  // field types and members
  using _sum_type =
    float;
  _sum_type sum;

  // setters for named parameter idiom
  Type & set__sum(
    const float & _arg)
  {
    this->sum = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    my_interfaces::srv::Vd_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const my_interfaces::srv::Vd_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<my_interfaces::srv::Vd_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<my_interfaces::srv::Vd_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      my_interfaces::srv::Vd_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<my_interfaces::srv::Vd_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      my_interfaces::srv::Vd_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<my_interfaces::srv::Vd_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<my_interfaces::srv::Vd_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<my_interfaces::srv::Vd_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__my_interfaces__srv__Vd_Response
    std::shared_ptr<my_interfaces::srv::Vd_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__my_interfaces__srv__Vd_Response
    std::shared_ptr<my_interfaces::srv::Vd_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Vd_Response_ & other) const
  {
    if (this->sum != other.sum) {
      return false;
    }
    return true;
  }
  bool operator!=(const Vd_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Vd_Response_

// alias to use template instance with default allocator
using Vd_Response =
  my_interfaces::srv::Vd_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace my_interfaces

namespace my_interfaces
{

namespace srv
{

struct Vd
{
  using Request = my_interfaces::srv::Vd_Request;
  using Response = my_interfaces::srv::Vd_Response;
};

}  // namespace srv

}  // namespace my_interfaces

#endif  // MY_INTERFACES__SRV__DETAIL__VD__STRUCT_HPP_

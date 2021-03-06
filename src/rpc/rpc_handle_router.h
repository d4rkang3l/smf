// Copyright (c) 2016 Alexander Gallego. All rights reserved.
//
#pragma once

#include <iostream>

#include "platform/macros.h"
#include "rpc/rpc_envelope.h"
#include "rpc/rpc_recv_context.h"
#include "rpc/rpc_service.h"

namespace smf {
/// \brief used to host many services
/// multiple services can use this class to handle the routing for them
///
class rpc_handle_router {
 public:
  rpc_handle_router() {}
  ~rpc_handle_router() {}
  void register_service(std::unique_ptr<rpc_service> s);

  seastar::future<> stop();

  virtual bool can_handle_request(const uint32_t &request_id);
  /// \brief actually makes the router dispatch
  virtual seastar::future<rpc_envelope> handle(rpc_recv_context &&recv);

  /// \brief multiple rpc_services can register w/ this  handle router
  void register_rpc_service(rpc_service *s);
  SMF_DISALLOW_COPY_AND_ASSIGN(rpc_handle_router);

 private:
  std::unordered_map<uint32_t, rpc_service_method_handle> dispatch_{};
  std::vector<std::unique_ptr<rpc_service>> services_{};

  friend std::ostream &operator<<(std::ostream &,
                                  const smf::rpc_handle_router &);
};
}  // namespace smf

// Copyright (c) 2017 Alexander Gallego. All rights reserved.
//
#pragma once

namespace smf {
struct rpc_server_stats {
  uint64_t active_connections{};
  uint64_t total_connections{};
  uint64_t in_bytes{};
  uint64_t out_bytes{};
  uint64_t bad_requests{};
  uint64_t no_route_requests{};
  uint64_t completed_requests{};
  uint64_t too_large_requests{};
};
}  // namespace smf

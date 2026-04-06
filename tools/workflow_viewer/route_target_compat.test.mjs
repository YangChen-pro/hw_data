import assert from 'node:assert/strict';

function routeTarget(item) {
  return item?.target || item?.next_node || '';
}

function renderTargetBadge(item) {
  const value = routeTarget(item);
  return value ? `next: ${value}` : 'next 未解析';
}

const resolvedNew = { target: 'step_2_check_port_vlan' };
const resolvedLegacy = { next_node: 'step_3_check_ip_interface' };
const unresolved = {};

assert.equal(routeTarget(resolvedNew), 'step_2_check_port_vlan');
assert.equal(routeTarget(resolvedLegacy), 'step_3_check_ip_interface');
assert.equal(routeTarget(unresolved), '');

assert.equal(renderTargetBadge(resolvedNew), 'next: step_2_check_port_vlan');
assert.equal(renderTargetBadge(resolvedLegacy), 'next: step_3_check_ip_interface');
assert.equal(renderTargetBadge(unresolved), 'next 未解析');

console.log('route_target_compat: ok');


#include "mem/cache/replacement_policies/lru_2.hh"

#include <memory>

#include "params/LRU2RP.hh"
#include "sim/cur_tick.hh"

namespace gem5
{

namespace replacement_policy
{

LRU2::LRU2(const Params &p)
    : LRU(p)
{
}
ReplaceableEntry* LRU2::getVictim(const ReplacementCandidates& candidates) const
{
    // There must be at least three replacement candidates
    assert(candidates.size() >= 3);

    // Initialize pointers for the top three MRU candidates
    ReplaceableEntry* mru_0 = nullptr;
    ReplaceableEntry* mru_1 = nullptr;
    ReplaceableEntry* mru_2 = nullptr;

    for (const auto& candidate : candidates) {
        auto lastTouchTick = std::static_pointer_cast<LRUReplData>(
            candidate->replacementData)->lastTouchTick;

        if (!mru_0 || lastTouchTick > std::static_pointer_cast<LRUReplData>(
                mru_0->replacementData)->lastTouchTick) {
            // Update MRU candidates
            mru_2 = mru_1;
            mru_1 = mru_0;
            mru_0 = candidate;
        } else if (!mru_1 || lastTouchTick > std::static_pointer_cast<LRUReplData>(
                mru_1->replacementData)->lastTouchTick) {
            // Update second MRU candidate
            mru_2 = mru_1;
            mru_1 = candidate;
        } else if (!mru_2 || lastTouchTick > std::static_pointer_cast<LRUReplData>(
                mru_2->replacementData)->lastTouchTick) {
            // Update third MRU candidate
            mru_2 = candidate;
        }
    }

    // Return the third most recently used candidate
    return mru_2;
}

} // namespace replacement_policy
} // namespace gem5

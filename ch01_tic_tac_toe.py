def onestep(player, env):
    board = env.board
    vanfn = player.valfn
    vals_for_candidates = [valfn for b1 in gen_candidates(board)]



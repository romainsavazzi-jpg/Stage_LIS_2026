def projection_point_sur_segment(C_x, C_y, A_x, A_y, B_x, B_y):
    AC_x = C_x - A_x
    AC_y = C_y - A_y
    AB_x = B_x - A_x
    AB_y = B_y - A_y
    BC_x = C_x - B_x
    BC_y = C_y - B_y

    s1 = AC_x * AB_x + AC_y * AB_y  # Premier scalaire entre AC et AB
    s2 = AB_x * BC_x + AB_y * BC_y  # Second scalaire entre AB et BC

    if (s1 * s2 > 0):  # si le produit est négatif ça veut dire qu'un des deux angles entre AC et AB ou entre AB et BC est négatif est l'autre positif
        return False

    return True

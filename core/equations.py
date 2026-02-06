import math
class MuskPsiEquation:
    """Psi_D = (Tc/dt) - G*(HI/dt) - W_Set"""
    def calculate_collapse(self, tech, human_will):
        psi_d = tech - human_will - 0.8
        return "EVASIÓN EXITOSA" if psi_d < 0 else "COLAPSO"

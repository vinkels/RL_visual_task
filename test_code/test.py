
import os

print os.listdir('images/HIGH_A')
    def set_bounds(self):
        B = np.matrix(0.5 * self.df['SC_gray'] + 0.25 * self.df['SC_blue_yellow'] + 0.25 * self.df['SC_red_green'])
        G = np.matrix(0.5 * self.df['CE_gray'] + 0.25 * self.df['CE_blue_yellow'] + 0.25 * self.df['CE_red_green'])
        # print(G)
        # print(B.dtype)
        del_BG = np.linalg.lstsq((max(B) - min(B)),(max(G)- min(G)))
        print(del_BG)
        # print(del_BG)
        B_norm = B * del_BG
        # print(B_norm)
        BG = np.hypot(B_norm, G)
        # BG = sqrt(B_norm.^2+G.^2)

        # B = 0.5 * Beta(:,1) + 0.25 * Beta(:,2) + 0.25 * Beta(:,3);
        # G = 0.5 *  Gamma(:,1) + 0.25 *  Gamma(:,2) + 0.25 * Gamma(:,3);
        # B_norm = B * (range(B)\range(G));
        # BG = sqrt(B_norm.^2+G.^2);
        # print(G)

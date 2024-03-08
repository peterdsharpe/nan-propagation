from juliacall import Main as jl

jl.include("tasopt_wing_weight_model.jl")
surfw_julia = jl.seval("surfw")


def surfw(
        po: float,
        b: float,
        bs: float,
        bo: float,
        co: float,
        zs: float,
        lambdat: float,
        lambdas: float,
        gammat: float,
        gammas: float,
        Nload: int,
        iwplan: int,
        We: float,
        neout: int,
        dyeout: float,
        neinn: int,
        dyeinn: float,
        Winn: float,
        Wout: float,
        dyWinn: float,
        dyWout: float,
        sweep: float,
        wbox: float,
        hboxo: float,
        hboxs: float,
        rh: float,
        fLt: float,
        tauweb: float,
        sigcap: float,
        sigstrut: float,
        Ecap: float,
        Eweb: float,
        Gcap: float,
        Gweb: float,
        rhoweb: float,
        rhocap: float,
        rhostrut: float,
        rhofuel: float,
) -> dict[str, float]:
    """
    Calculates Wing or Tail loads, stresses, weights of individual wing sections.
    Also returns the material gauges, torsional and bending stiffness.

    See [Geometry](@ref geometry),  [Wing/Tail Structures](@ref wingtail), and Section 2.7  of the [TASOPT Technical Description](@ref dreladocs).

    Args:
        po: Point where loads and stresses are calculated. [float]
        b: Wingspan. [float]
        bs: Spanwise location of the start of the taper. [float]
        bo: Spanwise location of the root chord. [float]
        co: Root chord length. [float]
        zs: Height of the strut attach point above wing. [float]
        lambdat: Tip chord ratio (tip chord / root chord). [float]
        lambdas: Start chord ratio (start chord / root chord). [float]
        gammat: Tip airfoil section shape exponent. [float]
        gammas: Start airfoil section shape exponent. [float]
        Nload: Number of loads (used to distribute engine loads). [int]
        iwplan: Indicates the presence of a strut. [int]
        We: Weight of the engine. [float]
        neout: Number of outboard engines. [int]
        dyeout: Distance between engines and the wingtip. [float]
        neinn: Number of inboard engines. [int]
        dyeinn: Distance between engines and the wing root. [float]
        Winn: Weight of inboard engines. [float]
        Wout: Weight of outboard engines. [float]
        dyWinn: Weight distribution of inboard engines. [float]
        dyWout: Weight distribution of outboard engines. [float]
        sweep: Sweep angle in degrees. [float]
        wbox: Width of the wing box. [float]
        hboxo: Height of the wing box at the root. [float]
        hboxs: Height of the wing box at the strut attach point. [float]
        rh: Fractional height of the wing box. [float]
        fLt: Factor applied to the tip load. [float]
        tauweb: Web material shear strength. [float]
        sigcap: Cap material axial compressive strength. [float]
        sigstrut: Strut material axial compressive strength. [float]
        Ecap: Cap material Young's modulus. [float]
        Eweb: Web material Young's modulus. [float]
        Gcap: Cap material shear modulus. [float]
        Gweb: Web material shear modulus. [float]
        rhoweb: Density of the web material. [float]
        rhocap: Density of the cap material. [float]
        rhostrut: Density of the strut material. [float]
        rhofuel: Density of the fuel. [float]

    Returns: A dictionary with key-value pairs:
        "Ss": Outboard section shear load. [float]
        "Ms": Outboard section moment. [float]
        "tbwebs": Web thickness at the strut attach point. [float]
        "tbcaps": Cap thickness at the strut attach point. [float]
        "EIcs": Combined cap and web bending stiffness at the strut attach point. [float]
        "EIns": Combined cap and web normal stiffness at the strut attach point. [float]
        "GJs": Combined cap and web shear stiffness at the strut attach point. [float]
        "So": Inboard section shear load. [float]
        "Mo": Inboard section moment. [float]
        "tbwebo": Web thickness at the wing root. [float]
        "tbcapo": Cap thickness at the wing root. [float]
        "EIco": Combined cap and web bending stiffness at the wing root. [float]
        "EIno": Combined cap and web normal stiffness at the wing root. [float]
        "GJo": Combined cap and web shear stiffness at the wing root. [float]
        "Astrut": Strut axial force. [float]
        "lsp": Strut length. [float]
        "cosLs": Cosine of the sweep angle at the strut attach point. [float]
        "Wscen": Weight of center section (inboard of the strut). [float]
        "Wsinn": Weight of the inner section. [float]
        "Wsout": Weight of the outer section. [float]
        "dxWsinn": Lateral distribution of inner section weight. [float]
        "dxWsout": Lateral distribution of outer section weight. [float]
        "dyWsinn": Vertical distribution of inner section weight. [float]
        "dyWsout": Vertical distribution of outer section weight. [float]
        "Wfcen": Weight of center section fuel. [float]
        "Wfinn": Weight of the inner section fuel. [float]
        "Wfout": Weight of the outer section fuel. [float]
        "dxWfinn": Lateral distribution of inner section fuel weight. [float]
        "dxWfout": Lateral distribution of outer section fuel weight. [float]
        "dyWfinn": Vertical distribution of inner section fuel weight. [float]
        "dyWfout": Vertical distribution of outer section fuel weight. [float]
        "Wweb": Weight of the wing web. [float]
        "Wcap": Weight of the wing cap. [float]
        "Wstrut": Weight of the strut. [float]
        "dxWweb": Lateral distribution of web weight. [float]
        "dxWcap": Lateral distribution of cap weight. [float]
        "dxWstrut": Lateral distribution of strut weight. [float]

    """

    (Ss, Ms, tbwebs, tbcaps, EIcs, EIns, GJs,
     So, Mo, tbwebo, tbcapo, EIco, EIno, GJo,
     Astrut, lstrutp, cosLs,
     Wscen, Wsinn, Wsout, dxWsinn, dxWsout, dyWsinn, dyWsout,
     Wfcen, Wfinn, Wfout, dxWfinn, dxWfout, dyWfinn, dyWfout,
     Wweb, Wcap, Wstrut, dxWweb, dxWcap, dxWstrut) = surfw_julia(
        po, b, bs, bo, co, zs, lambdat, lambdas, gammat, gammas, Nload, iwplan, We, neout, dyeout, neinn, dyeinn, Winn,
        Wout, dyWinn, dyWout, sweep, wbox, hboxo, hboxs, rh, fLt, tauweb, sigcap, sigstrut, Ecap, Eweb, Gcap, Gweb,
        rhoweb, rhocap, rhostrut, rhofuel
    )

    return {
        "Ss"      : Ss,
        "Ms"      : Ms,
        "tbwebs"  : tbwebs,
        "tbcaps"  : tbcaps,
        "EIcs"    : EIcs,
        "EIns"    : EIns,
        "GJs"     : GJs,
        "So"      : So,
        "Mo"      : Mo,
        "tbwebo"  : tbwebo,
        "tbcapo"  : tbcapo,
        "EIco"    : EIco,
        "EIno"    : EIno,
        "GJo"     : GJo,
        "Astrut"  : Astrut,
        "lsp"     : lstrutp,
        "cosLs"   : cosLs,
        "Wscen"   : Wscen,
        "Wsinn"   : Wsinn,
        "Wsout"   : Wsout,
        "dxWsinn" : dxWsinn,
        "dxWsout" : dxWsout,
        "dyWsinn" : dyWsinn,
        "dyWsout" : dyWsout,
        "Wfcen"   : Wfcen,
        "Wfinn"   : Wfinn,
        "Wfout"   : Wfout,
        "dxWfinn" : dxWfinn,
        "dxWfout" : dxWfout,
        "dyWfinn" : dyWfinn,
        "dyWfout" : dyWfout,
        "Wweb"    : Wweb,
        "Wcap"    : Wcap,
        "Wstrut"  : Wstrut,
        "dxWweb"  : dxWweb,
        "dxWcap"  : dxWcap,
        "dxWstrut": dxWstrut
    }


example_inputs = {
    "po"      : 114115.09920909579,
    "b"       : 37.53365209643924,
    "bs"      : 10.697090847485182,
    "bo"      : 3.6068,
    "co"      : 6.232215465340908,
    "zs"      : 3.9116,
    "lambdat" : 0.25,
    "lambdas" : 0.7,
    "gammat"  : 0.225,
    "gammas"  : 0.8665999999999999,
    "Nload"   : 3,
    "iwplan"  : 1,  # Replaced from 1
    "We"      : 30112.820951465743,
    "neout"   : 1,  # Replaced from 0
    "dyeout"  : 0.0,
    "neinn"   : 1,  # Replaced from 0
    "dyeinn"  : 0.0,
    "Winn"    : 49916.39401487996,
    "Wout"    : 70827.81179095857,
    "dyWinn"  : 78177.9198258339,
    "dyWout"  : 335574.9479578516,
    "sweep"   : 26.0,
    "wbox"    : 0.5,
    "hboxo"   : 0.1268,
    "hboxs"   : 0.1266,
    "rh"      : 0.75,
    "fLt"     : -0.05,
    "tauweb"  : 1.378951577903156e8,
    "sigcap"  : 2.0684273668547338e8,
    "sigstrut": 2.0684273668547338e8,
    "Ecap"    : 6.894757889515779e10,
    "Eweb"    : 6.894757889515779e10,
    "Gcap"    : 2.6518299575060688e10,
    "Gweb"    : 2.6518299575060688e10,
    "rhoweb"  : 2700.0,
    "rhocap"  : 2700.0,
    "rhostrut": 2700.0,
    "rhofuel" : 817.0
}

if __name__ == '__main__':
    outs = surfw(**example_inputs)

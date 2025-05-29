// Instruments.hpp

#pragma once
#include <string>
#include <vector>
#include <map>
#include <memory>
#include <array>

#include "dataclass/Macro.hpp"
#include "dataclass/KeyDPCM.hpp"

namespace ft::dataclass {

    class BaseInst {
    public:
        int index;
        std::string name;
        
        // virtual std::string get_str() = 0; // return a string representation
        virtual ~BaseInst() = default; // destrutor for inheritance
    };

    class Inst2A03 : public BaseInst {
    public:
        // int index;
        // std::string name;
        int seq_vol;
        int seq_arp;
        int seq_pit;
        int seq_hpi;
        int seq_dut;

        // macro objects stored here
        std::unique_ptr<Macro> vol_macro;
        std::unique_ptr<Macro> arp_macro;
        std::unique_ptr<Macro> pit_macro;
        std::unique_ptr<Macro> hpi_macro;
        std::unique_ptr<Macro> dut_macro;

        // unique to Inst2A03
        std::map<int, KeyDPCM> dpcm_sample_mappings;
        
        // TODO implement print self
    };

    class InstVRC6 : public BaseInst {
    public:
        // int index;
        // std::string name;
        int seq_vol;
        int seq_arp;
        int seq_pit;
        int seq_hpi;
        int seq_dut;

        // macro objects stored here
        std::unique_ptr<Macro> vol_macro;
        std::unique_ptr<Macro> arp_macro;
        std::unique_ptr<Macro> pit_macro;
        std::unique_ptr<Macro> hpi_macro;
        std::unique_ptr<Macro> dut_macro;
        
        // TODO implement print self
    };

    class InstVRC7 : public BaseInst {
    public:
        // int index;
        // std::string name;
        int patch;
        std::array<int, 8> registers;
        
        // TODO implement print self
    };

    class InstN163 : public BaseInst {
    public:
        // int index;
        // std::string name;
        int seq_vol;
        int seq_arp;
        int seq_pit;
        int seq_hpi;
        int seq_dut;

        // macro objects stored here
        std::unique_ptr<Macro> vol_macro;
        std::unique_ptr<Macro> arp_macro;
        std::unique_ptr<Macro> pit_macro;
        std::unique_ptr<Macro> hpi_macro;
        std::unique_ptr<Macro> dut_macro;

        // unique to N163
        int w_size;
        int w_pos;
        int w_count;
        std::map<int, std::vector<int>> waves;
        
        // TODO implement print self
    };

    class InstFDS : public BaseInst {
    public:
        // int index;
        // std::string name;
        bool mod_enable;
        int mod_speed;
        int mod_depth;
        int mod_delay;

        // FDS waves
        std::vector<int> wave;
        std::vector<int> mod;
        
        // FDS macro
        std::unique_ptr<Macro> vol_macro;
        std::unique_ptr<Macro> arp_macro;
        std::unique_ptr<Macro> pit_macro;
        
        // TODO implement print self
    };

    class InstS5B : public BaseInst {
    public:
        // int index;
        // std::string name;
        int seq_vol;
        int seq_arp;
        int seq_pit;
        int seq_hpi;
        int seq_dut;

        // macro objects stored here
        std::unique_ptr<Macro> vol_macro;
        std::unique_ptr<Macro> arp_macro;
        std::unique_ptr<Macro> pit_macro;
        std::unique_ptr<Macro> hpi_macro;
        std::unique_ptr<Macro> dut_macro;
        
        // TODO implement print self
    };

}

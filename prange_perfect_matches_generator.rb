database = "/Users/dsteelma/Desktop/patsy-prange_test.db"

batches = %w[
  pcb001 pcb002 pcb003 pcb004 pcb005 pcb006 pcb007 pcb008 pcb009 pcb010 pcb011
  pcb012 pcb013 pcb014 pcb015 pcb016 pcb017 pcb018 pcb019 pcb020 pcb021 pcb022
  pcb023 pcb024 pcb025 pcb026 pcb027 pcb028 pcb029 pcb030 pcb031 pcb032 pcb033
  pcb034 pcb035 pcb036 pcb037 pcb038 pcb039 pcb040 pcb041 pcb042 pcb043 pcb044
  pcb045 pcb046 pcb047 pcb048 pcb049 pcb050 pcb051 pcb052 pcb053 pcb054 pcb055
  pcb056 pcb057 pcb058 pcb059 pcb060 pcb061 pcb062 pcb063 pcb064 pcb065 pcb066
  pcb067 pcb068 pcb069 pcb070 pcb071 pcb073 pcb074 pcb075 pcb079 pcb080 pcb081
  pcb082 pcb083 pcb084 pcb085 pcb087 pcb091 pcb092 pcb093 pcb094 pcb095 pcb096
  pcb097 pcb098 pcb099 pcb100 pcb101 pcb102 pcb103 pcb104 pcb105 pcb106 pcb107
  pcb108 pcb109 pcb110 pcb111 pcb112 pcb113 pcb114 pcb115 pcb116 pcb118 pcb119
  pcb120 pcb121 pcb122 pcb123 pcb124 pcb125 pcb126 pcb127 pcb128 pcb129 pcb130
  pcb131 pcb132 pcb133 pcb134 pcb135 pcb136 pcb137 pcb138 pcb139 pcb140 pcb141
  pcb142 pcb143 pcb144 pcb145 pcb146 pgb001 pgb002 pgb003 pgb004 pgb005 pgb006
  pgb007 pgb008 pgb009 pgb010 pgb011 pgb012 pgb013 pgb014 pgb015 pgb016 pgb017
  pgb018 pgb019 pgb020 pgb021 pgb022 pgb023 pgb024 pgb025 pgb026 pgb027 pgb028
  pgb029 pgb030 pgb031 pgb032 pgb033 pgb034 pgb035 pgb036 pgb037 pgb038 pgb039
  pgb040 pgb041 pgb042 pgb043 pgb044 pgb045 pgb046 pgb047 pgb048 pgb049 pgb050
  pgb051 pgb052 pgb053 pgb054 pgb055 pgb056 pgb057 pgb058 pgb059 pgb060 pgb061
  pgb062 pgb063 pgb064 pgb065 pgb066 pgb067 pgb068 pgb069 pgb070 pgb071 pgb072
  pgb073 pgb074 pgb075 pgb076 pgb077 pgb078 pgb079 pgb080 pgb081 pgb082 pgb083
  pgb084 pgb085 pgb086 pgb087 pgb089 pgb090 pgb091 pgb092 pgb093 pgb094 pgb095
  pgb096 pgb097 pgb098 pgb099 pgb100 pgb101 pgb102 pgb103 pgb122 pgb123 pgb124
  pgb125 pgb126 pgb127 pgb128 pgb129 pgb130 pgb131 pgb132 pgb133 pgb134 pgb135
  pgb136 pgb137 pgb138 pgb139 pgb140 pgb141 pgb142 pgb143 pgb144 pgb145 pgb146
  pgb147 pgb148 pgb149 pgb150 pgb151 pgb152 pgb153 pgb154 pgb155 pgb156 pgb157
  pgb158 pgb159 pgb160 pgb161 pgb162 pgb163 pgb164 pgb165 pgb166 pgb167 pgb168
  pgb169 pgb170 pgb171 pgb172 pgb173 pgb174 pgb175 pgb176 pgb177 pgb178 pgb179
  pgb180 pgb181 pgb182 pgb183 pgb184 pgb185 pgb186 pgb187 pgb188 pgb189 pgb190
  pgb191 pgb192 pgb193 pgb194 pgb195 pgb196 pgb197 pgb198 pgb199 pgb200 pgb201
  pgb202 pgb203 pgb204 pgb205 pgb206 pgb207 pgb208 pgb209 pgb210 pgb211 pgb212
  pgb213 pgb214 pgb215 pgb216 pgb217 pgb218 pgb219 pgb220 pgb221 pgb222 pgb223
  pgb224 pgb225 pgb226 pgb227 pgb228 pgb229 pgb230 pgb231 pgb232 pgb233 pgb234
  pgb235 pgb236
]

batches.each do |batch|
  puts "echo #{batch}"
  puts "time python3 -m patsy --database #{database} find_perfect_matches --batch #{batch}"
end
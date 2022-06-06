<template>
  <v-container>
    <v-row class="text-center d-flex justify-center mb-6">
      <v-col cols="12" class="">
        <v-img
          :src="require('../assets/logo.jpg')"
          class="my-3"
          contain
          height="200"
        />
        <h1 class="display-2 font-weight-bold mb-3">PonzInspect</h1>
      </v-col>
      <v-col cols="6">
        <v-textarea
          v-model="opcode"
          row-height="10"
          rows="28"
          solo
          placeholder="OPCODE HERE"
          outlined
        >
        </v-textarea>
      </v-col>
      <v-col cols="6" align-self="center">
        <v-btn
          @click="submit"
          :disabled="!opcode"
          v-if="detect_status === 0"
          icon
          color="green"
        >
          <v-icon size="150">mdi-shield-bug-outline</v-icon>
        </v-btn>
        <v-progress-circular
          v-if="detect_status === 1"
          :value="is_ponzi?score:100"
          :rotate="-90"
          :size="200"
          :width="15"
          :color="progressColor"
        >
          <h1>{{ is_ponzi ? "Ponzi" : "Safe" }}</h1>
        </v-progress-circular>

      </v-col>
      <v-col>
        <v-btn @click="reset" v-show="detect_status===1">RESET</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
export default {
  name: "DetectorComponent",

  data: () => ({
    opcode: "",
    detect_status: 0,
    progressing: false,
    is_ponzi: true,
    score: 0,
  }),

  methods: {
    reset(){
      this.progressing = false
      this.opcode = ""
      this.score = 0 
      this.detect_status = 0
    },
    setVal(label, score) {
      this.is_ponzi = label;
      this.score = score.toFixed(2) * 100;
    },
    submit() {
      this.progressing = true;
      axios
        .post("http://127.0.0.1:5000/api/ponzi", this.opcode.trim())
        .then((res) => {
          setTimeout(() => {
            this.is_ponzi = res.data.label;
            this.score = Math.round(res.data.prob * 100);
          }, 300);
          this.progressing = false;
          this.detect_status = 1;
        })
        .catch(() => {
          alert("發生錯誤");
          this.detect_status = 0;
          this.progressing = false;
        });
    },
  },
  computed: {
    progressColor() {
      if (!this.is_ponzi) {
        return "green";
      }
      if (this.score < 60) {
        return "yellow";
      } else if (this.score < 80) {
        return "orange";
      } else {
        return "red";
      }
    },
  },
};
</script>

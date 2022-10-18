wow = new WOW({
  boxClass:     'wow',      // default
  animateClass: 'animated', // default
  offset:       0,          // default
  mobile:       true,       // default
  live:         true        // default
})
wow.init();

function checkVelocityArrowsAnimation(countAnimation, isAnimationEnabled){
  if(!isAnimationEnabled[0]){
    document.getElementsByClassName("turnLogo1")[0].style.visibility = "hidden";
    document.getElementsByClassName("turnLogo2")[0].style.visibility = "hidden";
    document.getElementsByClassName("turnLogo1Liquid")[0].style.visibility = "hidden";
    document.getElementsByClassName("turnLogo2Liquid")[0].style.visibility = "hidden";
    countAnimation[0] = 2;
  } else {
    if(countAnimation[0] < 2){
      countAnimation[0] = countAnimation[0] + 1;
    } else {
      if(countAnimation[0] == 2){
        document.getElementsByClassName("turnLogo1")[0].style.visibility = "visible";
        document.getElementsByClassName("turnLogo2")[0].style.visibility = "hidden";
        document.getElementsByClassName("turnLogo1Liquid")[0].style.visibility = "visible";
        document.getElementsByClassName("turnLogo2Liquid")[0].style.visibility = "hidden";
        countAnimation[0] = countAnimation[0] + 1;
      } else {
        document.getElementsByClassName("turnLogo1")[0].style.visibility = "hidden";
        document.getElementsByClassName("turnLogo2")[0].style.visibility = "visible";
        document.getElementsByClassName("turnLogo1Liquid")[0].style.visibility = "hidden";
        document.getElementsByClassName("turnLogo2Liquid")[0].style.visibility = "visible";
        countAnimation[0] = countAnimation[0] - 1;
      }
    }
  }
}

function checkVelocityBubblesAnimation(countAnimation, isAnimationEnabled){
  if(!isAnimationEnabled[1]){
    document.getElementsByClassName("bubblesLiquid1")[0].style.visibility = "hidden";
    document.getElementsByClassName("bubblesLiquid2")[0].style.visibility = "hidden";
    document.getElementsByClassName("bubblesLiquid3")[0].style.visibility = "hidden";
    document.getElementsByClassName("bubblesLiquid4")[0].style.visibility = "hidden";
    document.getElementsByClassName("bubblesLiquid5")[0].style.visibility = "hidden";
    document.getElementsByClassName("bubblesLiquid6")[0].style.visibility = "hidden";
    countAnimation[1] = 2;
  } else {
    if(countAnimation[1] < 2){
      countAnimation[1] = countAnimation[1] + 1;
    } else {
      if(countAnimation[1] == 2){
        document.getElementsByClassName("bubblesLiquid1")[0].style.visibility = "visible";
        document.getElementsByClassName("bubblesLiquid2")[0].style.visibility = "visible";
        document.getElementsByClassName("bubblesLiquid3")[0].style.visibility = "hidden";
        document.getElementsByClassName("bubblesLiquid4")[0].style.visibility = "hidden";
        document.getElementsByClassName("bubblesLiquid5")[0].style.visibility = "hidden";
        document.getElementsByClassName("bubblesLiquid6")[0].style.visibility = "hidden";
        countAnimation[1] = countAnimation[1] + 1;
      } else {
        if(countAnimation[1] == 3){
          document.getElementsByClassName("bubblesLiquid1")[0].style.visibility = "visible";
          document.getElementsByClassName("bubblesLiquid2")[0].style.visibility = "visible";
          document.getElementsByClassName("bubblesLiquid3")[0].style.visibility = "visible";
          document.getElementsByClassName("bubblesLiquid4")[0].style.visibility = "visible";
          document.getElementsByClassName("bubblesLiquid5")[0].style.visibility = "hidden";
          document.getElementsByClassName("bubblesLiquid6")[0].style.visibility = "hidden";
          countAnimation[1] = countAnimation[1] + 1;
        } else {
          if(countAnimation[1] == 4){
            document.getElementsByClassName("bubblesLiquid1")[0].style.visibility = "visible";
            document.getElementsByClassName("bubblesLiquid2")[0].style.visibility = "visible";
            document.getElementsByClassName("bubblesLiquid3")[0].style.visibility = "visible";
            document.getElementsByClassName("bubblesLiquid4")[0].style.visibility = "visible";
            document.getElementsByClassName("bubblesLiquid5")[0].style.visibility = "visible";
            document.getElementsByClassName("bubblesLiquid6")[0].style.visibility = "visible";
            countAnimation[1] = countAnimation[1] + 1;
          } else {
            if(countAnimation[1] == 5){
              document.getElementsByClassName("bubblesLiquid1")[0].style.visibility = "hidden";
              document.getElementsByClassName("bubblesLiquid2")[0].style.visibility = "hidden";
              document.getElementsByClassName("bubblesLiquid3")[0].style.visibility = "visible";
              document.getElementsByClassName("bubblesLiquid4")[0].style.visibility = "visible";
              document.getElementsByClassName("bubblesLiquid5")[0].style.visibility = "visible";
              document.getElementsByClassName("bubblesLiquid6")[0].style.visibility = "visible";
              countAnimation[1] = countAnimation[1] + 1;
            } else {
              if(countAnimation[1] == 6){
                document.getElementsByClassName("bubblesLiquid1")[0].style.visibility = "hidden";
                document.getElementsByClassName("bubblesLiquid2")[0].style.visibility = "hidden";
                document.getElementsByClassName("bubblesLiquid3")[0].style.visibility = "hidden";
                document.getElementsByClassName("bubblesLiquid4")[0].style.visibility = "hidden";
                document.getElementsByClassName("bubblesLiquid5")[0].style.visibility = "visible";
                document.getElementsByClassName("bubblesLiquid6")[0].style.visibility = "visible";
                countAnimation[1] = countAnimation[1] + 1;
              } else { 
                if(countAnimation[1] == 7) {
                  document.getElementsByClassName("bubblesLiquid1")[0].style.visibility = "hidden";
                  document.getElementsByClassName("bubblesLiquid2")[0].style.visibility = "hidden";
                  document.getElementsByClassName("bubblesLiquid3")[0].style.visibility = "hidden";
                  document.getElementsByClassName("bubblesLiquid4")[0].style.visibility = "hidden";
                  document.getElementsByClassName("bubblesLiquid5")[0].style.visibility = "hidden";
                  document.getElementsByClassName("bubblesLiquid6")[0].style.visibility = "hidden";
                  countAnimation[1] = 2;
                }
              } 
            }
          }
        }
      }
    }
  }
}

function checkTemperatureAnimation(countAnimation, isAnimationEnabled){
  if(!isAnimationEnabled[2]){
    document.getElementsByClassName("temperatureSensor")[0].style.visibility = "hidden";
    document.getElementsByClassName("fluidIn")[0].style.visibility = "hidden";
    document.getElementsByClassName("fluidDirection1")[0].style.visibility = "hidden";
    document.getElementsByClassName("fluidDirection2")[0].style.visibility = "hidden";
    document.getElementsByClassName("fluidDirection3")[0].style.visibility = "hidden";
    document.getElementsByClassName("fluidDirection4")[0].style.visibility = "hidden";
    document.getElementsByClassName("fluidOut")[0].style.visibility = "hidden";
    countAnimation[2] = 2;
  } else {
    if(countAnimation[2] < 2){
      countAnimation[2] = countAnimation[2] + 1;
    } else {
      if(countAnimation[2] == 2){
        document.getElementsByClassName("temperatureSensor")[0].style.visibility = "visible";
        document.getElementsByClassName("fluidIn")[0].style.visibility = "visible";
        document.getElementsByClassName("fluidDirection1")[0].style.visibility = "hidden";
        document.getElementsByClassName("fluidDirection2")[0].style.visibility = "hidden";
        document.getElementsByClassName("fluidDirection3")[0].style.visibility = "hidden";
        document.getElementsByClassName("fluidDirection4")[0].style.visibility = "hidden";
        document.getElementsByClassName("fluidOut")[0].style.visibility = "hidden";
        countAnimation[2] = countAnimation[2] + 1;
      } else {
        if(countAnimation[2] == 3){
          document.getElementsByClassName("temperatureSensor")[0].style.visibility = "visible";
          document.getElementsByClassName("fluidIn")[0].style.visibility = "visible";
          document.getElementsByClassName("fluidDirection1")[0].style.visibility = "visible";
          document.getElementsByClassName("fluidDirection2")[0].style.visibility = "hidden";
          document.getElementsByClassName("fluidDirection3")[0].style.visibility = "hidden";
          document.getElementsByClassName("fluidDirection4")[0].style.visibility = "hidden";
          document.getElementsByClassName("fluidOut")[0].style.visibility = "hidden";
          countAnimation[2] = countAnimation[2] + 1;
        } else {
          if(countAnimation[2] == 4){
            document.getElementsByClassName("temperatureSensor")[0].style.visibility = "visible";
            document.getElementsByClassName("fluidIn")[0].style.visibility = "visible";
            document.getElementsByClassName("fluidDirection1")[0].style.visibility = "visible";
            document.getElementsByClassName("fluidDirection2")[0].style.visibility = "visible";
            document.getElementsByClassName("fluidDirection3")[0].style.visibility = "hidden";
            document.getElementsByClassName("fluidDirection4")[0].style.visibility = "hidden";
            document.getElementsByClassName("fluidOut")[0].style.visibility = "hidden";
            countAnimation[2] = countAnimation[2] + 1;
          } else {
            if(countAnimation[2] == 5){
              document.getElementsByClassName("temperatureSensor")[0].style.visibility = "visible";
              document.getElementsByClassName("fluidIn")[0].style.visibility = "visible";
              document.getElementsByClassName("fluidDirection1")[0].style.visibility = "visible";
              document.getElementsByClassName("fluidDirection2")[0].style.visibility = "visible";
              document.getElementsByClassName("fluidDirection3")[0].style.visibility = "visible";
              document.getElementsByClassName("fluidDirection4")[0].style.visibility = "hidden";
              document.getElementsByClassName("fluidOut")[0].style.visibility = "hidden";
              countAnimation[2] = countAnimation[2] + 1;
            } else {
              if(countAnimation[2] == 6){
                document.getElementsByClassName("temperatureSensor")[0].style.visibility = "visible";
                document.getElementsByClassName("fluidIn")[0].style.visibility = "visible";
                document.getElementsByClassName("fluidDirection1")[0].style.visibility = "visible";
                document.getElementsByClassName("fluidDirection2")[0].style.visibility = "visible";
                document.getElementsByClassName("fluidDirection3")[0].style.visibility = "visible";
                document.getElementsByClassName("fluidDirection4")[0].style.visibility = "visible";
                document.getElementsByClassName("fluidOut")[0].style.visibility = "hidden";
                countAnimation[2] = countAnimation[2] + 1;
              } else { 
                if(countAnimation[2] == 7) {
                  document.getElementsByClassName("temperatureSensor")[0].style.visibility = "visible";
                  document.getElementsByClassName("fluidIn")[0].style.visibility = "visible";
                  document.getElementsByClassName("fluidDirection1")[0].style.visibility = "visible";
                  document.getElementsByClassName("fluidDirection2")[0].style.visibility = "visible";
                  document.getElementsByClassName("fluidDirection3")[0].style.visibility = "visible";
                  document.getElementsByClassName("fluidDirection4")[0].style.visibility = "visible";
                  document.getElementsByClassName("fluidOut")[0].style.visibility = "visible";
                  countAnimation[2] = countAnimation[2] + 1;
                } else {
                  if(countAnimation[2] == 8) {
                    document.getElementsByClassName("temperatureSensor")[0].style.visibility = "visible";
                    document.getElementsByClassName("fluidIn")[0].style.visibility = "hidden";
                    document.getElementsByClassName("fluidDirection1")[0].style.visibility = "hidden";
                    document.getElementsByClassName("fluidDirection2")[0].style.visibility = "hidden";
                    document.getElementsByClassName("fluidDirection3")[0].style.visibility = "hidden";
                    document.getElementsByClassName("fluidDirection4")[0].style.visibility = "hidden";
                    document.getElementsByClassName("fluidOut")[0].style.visibility = "hidden";
                    countAnimation[2] = 2;
                  }
                } 
              }
            }
          }
        }
      }
    }
  }
}

function checkPotentialAnimation(countAnimation, isAnimationEnabled){
  if(!isAnimationEnabled[3]){
    document.getElementsByClassName("potentialSensor")[0].style.visibility = "hidden";
    document.getElementsByClassName("dropsBase2")[0].style.visibility = "hidden";
    document.getElementsByClassName("dropsAcid2")[0].style.visibility = "hidden";
    document.getElementsByClassName("dropsBase1")[0].style.visibility = "hidden";
    document.getElementsByClassName("dropsAcid1")[0].style.visibility = "hidden";
    countAnimation[3] = 2;
  } else {
    if(countAnimation[3] < 2){
      countAnimation[3] = countAnimation[3] + 1;
    } else {
      if(countAnimation[3] == 2){
        document.getElementsByClassName("potentialSensor")[0].style.visibility = "visible";
        document.getElementsByClassName("dropsBase2")[0].style.visibility = "visible";
        document.getElementsByClassName("dropsAcid2")[0].style.visibility = "visible";
        document.getElementsByClassName("dropsBase1")[0].style.visibility = "hidden";
        document.getElementsByClassName("dropsAcid1")[0].style.visibility = "hidden";
        countAnimation[3] = countAnimation[3] + 1;
      } else {
        if(countAnimation[3] == 3){
          document.getElementsByClassName("potentialSensor")[0].style.visibility = "visible";
          document.getElementsByClassName("dropsBase2")[0].style.visibility = "visible";
          document.getElementsByClassName("dropsAcid2")[0].style.visibility = "visible";
          document.getElementsByClassName("dropsBase1")[0].style.visibility = "visible";
          document.getElementsByClassName("dropsAcid1")[0].style.visibility = "visible";
          countAnimation[3] = countAnimation[3] + 1;
        } else {
          if(countAnimation[3] == 4){
            document.getElementsByClassName("potentialSensor")[0].style.visibility = "visible";
            document.getElementsByClassName("dropsBase2")[0].style.visibility = "hidden";
            document.getElementsByClassName("dropsAcid2")[0].style.visibility = "hidden";
            document.getElementsByClassName("dropsBase1")[0].style.visibility = "visible";
            document.getElementsByClassName("dropsAcid1")[0].style.visibility = "visible";
            countAnimation[3] = countAnimation[3] + 1;
          } else {
            if(countAnimation[3] == 5){
              document.getElementsByClassName("potentialSensor")[0].style.visibility = "visible";
              document.getElementsByClassName("dropsBase2")[0].style.visibility = "hidden";
              document.getElementsByClassName("dropsAcid2")[0].style.visibility = "hidden";
              document.getElementsByClassName("dropsBase1")[0].style.visibility = "hidden";
              document.getElementsByClassName("dropsAcid1")[0].style.visibility = "hidden";
              countAnimation[3] = 2;
            }
          }
        }
      }
    }
  }
}

function checkGeneralAnimations(countAnimation, isAnimationEnabled){
  isAnimationEnabled[0] = (document.getElementById('velStatusInfo').innerHTML == "Velocity Status: RUNNING")
  isAnimationEnabled[1] = (document.getElementById('velStatusInfo').innerHTML == "Velocity Status: RUNNING")
  isAnimationEnabled[2] = (document.getElementById('temStatusInfo').innerHTML == "Temperature Status: RUNNING")
  isAnimationEnabled[3] = (document.getElementById('potStatusInfo').innerHTML == "Potential Hydrogen Status: RUNNING")
  checkVelocityArrowsAnimation(countAnimation, isAnimationEnabled);
  checkVelocityBubblesAnimation(countAnimation, isAnimationEnabled);
  checkTemperatureAnimation(countAnimation, isAnimationEnabled);
  checkPotentialAnimation(countAnimation, isAnimationEnabled);
}
